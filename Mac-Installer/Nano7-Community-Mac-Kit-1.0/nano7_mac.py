#!/usr/bin/env python3
"""Conservative, file-only installer for already-untethered nano 7G devices.

This DOES NOT install or verify firmware. Does not issue SCSI commands, repartition,
change media libraries, alter IconState.plist, or run programs on the device.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import plistlib
import shutil
import subprocess
import sys
import tempfile
import traceback

BASE=Path(__file__).resolve().parent
PAYLOAD=BASE/'Payload'
MANIFEST=BASE/'payload-manifest.json'
HOME=Path.home()
DEST=HOME/'Desktop'/'Nano7-App-Backups'
ACTIVATION=Path('Apps/Startup/resident-B.active')
EXPECTED={
    'Apps/Startup/ab.hbapp','Apps/Startup/resident-A.hbapp',
    'Apps/Startup/resident-B.hbapp','Apps/Startup/resident-B.active',
    'Apps/AllApps.pack','Apps/AllApps-B.pack',
    'Apps/Executables/Calculator.hbapp','Apps/Executables/Contacts.hbapp',
    'Apps/Executables/Chess.hbapp','Apps/Executables/Golf.hbapp',
    'Apps/Icons/Calculator.bin','Apps/Icons/Contacts.bin',
    'Apps/Icons/Chess.bin','Apps/Icons/Golf.bin'
}

class Stop(Exception):pass

def digest(path:Path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()

def safe_rel(name):
    p=Path(name)
    if p.is_absolute() or '..' in p.parts or p.parts[:1]!=('Apps',) or not all(x and x!='.' for x in p.parts):
        raise Stop('Illegal payload path: '+name)
    return p

def verify_payload():
    if not MANIFEST.is_file():raise Stop('payload-manifest.json missing.')
    m=json.loads(MANIFEST.read_text(encoding='utf-8'))
    entries=m.get('files',{})
    if set(entries)!=EXPECTED: raise Stop('Payload manifest has missing/extra files; refusing.')
    files={str(p.relative_to(PAYLOAD)) for p in PAYLOAD.rglob('*') if p.is_file()}
    if files!=EXPECTED: raise Stop('Payload folder has missing/extra files; refusing.')
    for rel,rec in entries.items():
        p=PAYLOAD/safe_rel(rel)
        if p.is_symlink() or p.stat().st_size!=rec['size'] or digest(p)!=rec['sha256']:
            raise Stop('Payload integrity FAILED: '+rel)
    return m

def info_for(path:Path):
    p=subprocess.run(['/usr/sbin/diskutil','info','-plist',str(path)],capture_output=True)
    if p.returncode:raise Stop('Cannot identify selected disk using diskutil.')
    try: data=plistlib.loads(p.stdout)
    except Exception as e: raise Stop('Cannot parse macOS diskutil output.') from e
    size=int(data.get('TotalSize') or 0)
    uuid=str(data.get('VolumeUUID') or data.get('DiskUUID') or '').strip().upper()
    removable=data.get('Removable')
    internal=data.get('Internal')
    if not uuid:raise Stop('Could not obtain stable device UUID. Do not proceed.')
    if size<12_000_000_000 or size>18_000_000_000: raise Stop('Unexpected volume size for a 16 GB nano 7G.')
    if removable is not True or internal is not False:
        raise Stop('Volume is not reported as external/removable. Refusing to modify.')
    return dict(uuid=uuid,size=size,filesystem=str(data.get('FilesystemType') or data.get('Content') or 'unknown'),disk=str(data.get('DeviceIdentifier') or 'unknown'),name=str(path.name))

def detect():
    if sys.platform!='darwin':raise Stop('Device installation requires macOS. Self-test works elsewhere.')
    root=Path('/Volumes')
    options=[]
    for vol in root.iterdir():
        if not vol.is_dir() or vol.is_symlink():continue
        if not (vol/'iPod_Control'/'Device').is_dir():continue
        try: d=info_for(vol)
        except Stop:continue
        options.append((vol,d))
    if len(options)!=1:
        raise Stop(f'Exactly ONE mounted 16 GB removable iPod is required. Found {len(options)} qualifying iPod(s). Disconnect other iPods, reconnect one nano in normal mode.')
    return options[0]

def secure_target(root:Path, rel:Path):
    # Reject all symlink ancestors, including the file itself, to prevent path escapes.
    curr=root
    if curr.is_symlink():raise Stop('Volume is a symbolic link.')
    for part in rel.parts:
        curr=curr/part
        if curr.is_symlink():raise Stop('Unsafe symbolic link at '+str(curr))
    return curr

def ensure_parent(root:Path, rel:Path):
    secure_target(root,rel)
    (root/rel).parent.mkdir(parents=True,exist_ok=True)
    secure_target(root,rel)

def atomic_copy(source:Path,target:Path):
    fd,temp=tempfile.mkstemp(prefix='.nano7-stage-',dir=str(target.parent))
    try:
        with os.fdopen(fd,'wb') as f, source.open('rb') as src:
            shutil.copyfileobj(src,f,1024*1024)
            f.flush();os.fsync(f.fileno())
        os.replace(temp,target)
    finally:
        if os.path.lexists(temp):os.unlink(temp)

def backup(root:Path, device:dict, m:dict):
    DEST.mkdir(parents=True,exist_ok=True)
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d-%H%M%S-%f')
    folder=DEST/f'Nano7-{device["uuid"][:8]}-{stamp}'
    folder.mkdir(mode=0o700)
    old={}
    for rel in sorted(m['files']):
        src=secure_target(root,safe_rel(rel))
        if src.exists():
            if not src.is_file():raise Stop('Expected regular file, found other type: '+rel)
            out=folder/'Original'/rel
            out.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(src,out)
            if digest(src)!=digest(out):raise Stop('Backup verification failed for '+rel)
            old[rel]={'existed':True,'sha256':digest(src),'size':src.stat().st_size}
        else:old[rel]={'existed':False}
    rec={'format':1,'device_uuid':device['uuid'],'device_size':device['size'],
         'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
         'note':'Only pre-existing files in the 14 paths are backed up; NOT a full 16 GB iPod backup.',
         'original_files':old,'installed_files':m['files'],'status':'backup-only'}
    (folder/'backup.json').write_text(json.dumps(rec,indent=2)+'\n')
    return folder,rec

def save_receipt(folder,receipt):
    tmp=folder/'backup.json.tmp'
    tmp.write_text(json.dumps(receipt,indent=2)+'\n')
    os.replace(tmp,folder/'backup.json')

def put_files(root:Path,m:dict):
    names=[x for x in sorted(m['files']) if x!=str(ACTIVATION)]+[str(ACTIVATION)]
    done=[]
    for rel in names:
        p=safe_rel(rel)
        ensure_parent(root,p)
        dest=secure_target(root,p)
        atomic_copy(PAYLOAD/p,dest)
        done.append(rel)
        if dest.stat().st_size!=m['files'][rel]['size'] or digest(dest)!=m['files'][rel]['sha256']:
            raise Stop('Read-back mismatch for '+rel)
    return done

def restore_files(root:Path,folder:Path,rec:dict,verify_current=False):
    changes=[]
    for rel,original in rec['original_files'].items():
        target=secure_target(root,safe_rel(rel))
        if verify_current and target.exists():
            if not target.is_file():
                raise Stop('Non-file changed since install: '+rel)
            actual=digest(target)
            allowed={rec['installed_files'][rel]['sha256']}
            if original.get('existed'):allowed.add(original['sha256'])
            if actual not in allowed:
                raise Stop('File was modified by another tool; refusing to overwrite: '+rel)
    # Deactivate before restoring the rest.
    names=[str(ACTIVATION)]+[x for x in sorted(rec['original_files']) if x!=str(ACTIVATION)]
    for rel in names:
        original=rec['original_files'][rel]
        target=secure_target(root,safe_rel(rel))
        if original['existed']:
            src=folder/'Original'/rel
            if not src.is_file() or digest(src)!=original['sha256']:
                raise Stop('Backup is damaged or missing: '+rel)
            ensure_parent(root,safe_rel(rel))
            atomic_copy(src,target)
            if digest(target)!=original['sha256']:raise Stop('Restore read-back failed: '+rel)
        else:
            if target.exists():
                if not target.is_file():raise Stop('Unexpected non-file at '+rel)
                target.unlink()
        changes.append(rel)
    return changes

def show_header(vol,device):
    print('\nConnected iPod volume :',vol)
    print('macOS volume ID       :',device['uuid'])
    print('Disk ID               :',device['disk'])
    print('Filesystem            :',device['filesystem'])
    print('Capacity              :',f'{device["size"]/1e9:.2f} GB')
    print('Hardware year         : NOT automatically verifiable from A1446/volume alone')


def select_year():
    print('\nThe iPod nano 7G has TWO hardware revisions. Choose by actual device history/colour, not merely by A1446.')
    print('  1 = 2012 generation (including 2013 colours)')
    print('  2 = 2015 colour refresh')
    s=input('Revision [1/2; other cancels]: ').strip()
    if s not in ('1','2'):raise Stop('Cancelled.')
    return '2012' if s=='1' else '2015'

def install(vol,device,m,year):
    print('\nThis will install FOUR apps: Calculator, Contacts, Chess, Golf.')
    print('This is FILE COPY ONLY. It CANNOT install the required patched/untethered firmware.')
    print('It REPLACES 14 specific paths within /Apps, including startup loaders and app packs.')
    print('Other installed custom apps may disappear from the Home Screen; backup/rollback is provided.')
    print('WARNING: A mismatched startup loader could crash or bootloop the iPod on restart.')
    print('2012 compatibility with this EXACT custom loader is NOT hardware-verified.')
    print('No full-device image backup is created. A firmware rollback is not possible with this kit.')
    if input('\nIs compatible UNTETHERED 7G firmware already running? Type YES to confirm: ').strip()!='YES':raise Stop('No files changed. First follow firmware preparation guide.')
    phrase=f'INSTALL {year} FOUR APPS'
    if input(f'To begin local backup and file copy, type {phrase}: ').strip()!=phrase:
        raise Stop('Cancelled; no files changed.')
    # Identity immediately before writes
    current=info_for(vol)
    if current['uuid']!=device['uuid'] or current['size']!=device['size']:
        raise Stop('Device changed since detection; refusing.')
    folder,rec=backup(vol,device,m)
    print('Backup of affected paths:',folder)
    try:
        rec['status']='write-in-progress';save_receipt(folder,rec)
        put_files(vol,m)
        rec['status']='installed';rec['year_selected_by_user']=year
        save_receipt(folder,rec)
    except Exception:
        print('INSTALL FAILED. Attempting to restore original files from the local backup...')
        try:
            restore_files(vol,folder,rec,verify_current=False)
            rec['status']='restored-after-install-error';save_receipt(folder,rec)
            print('Original tracked files were restored. Other device contents untouched.')
        except Exception as rollback_error:
            rec['status']='ROLLBACK-FAILED-MANUAL-HELP-REQUIRED';save_receipt(folder,rec)
            print('AUTOMATIC RESTORE FAILED:',rollback_error)
            print('STOP. Do not disconnect during an active write; preserve backup and logs.')
        raise
    print('\nINSTALL FILES VERIFIED. This is NOT verification of the code running on hardware.')
    print('Eject safely; on the nano, open Music and return Home, then test each app.')
    print('If apps do not show, confirm the firmware/loader startup hook is functional.')
    print('Local backup folder:',folder)

def verify(vol,device,m):
    show_header(vol,device)
    errors=[]
    for rel,meta in m['files'].items():
        f=secure_target(vol,safe_rel(rel))
        if not f.is_file() or f.stat().st_size!=meta['size'] or digest(f)!=meta['sha256']:
            errors.append(rel)
    if errors:
        print('Some expected files are missing/changed:')
        for x in errors:print('  -',x)
        raise Stop('File verification failed. Run Restore if this was installed by this kit.')
    print('\nPASS: All 14 installed files match the ZIP byte-for-byte.')
    print('This cannot prove the firmware is patched or the apps launch on hardware.')

def restore_menu(vol,device):
    if not DEST.exists():raise Stop('No backup folder exists on this Mac.')
    folders=[]
    for folder in sorted(DEST.iterdir(),reverse=True):
        meta=folder/'backup.json'
        if folder.is_symlink() or not meta.is_file():continue
        try:r=json.loads(meta.read_text())
        except Exception:continue
        if (r.get('device_uuid')==device['uuid'] and r.get('format')==1
                and set(r.get('original_files',{}))==EXPECTED
                and set(r.get('installed_files',{}))==EXPECTED
                and r.get('status') in ('installed','write-in-progress','ROLLBACK-FAILED-MANUAL-HELP-REQUIRED')):
            folders.append((folder,r))
    if not folders:raise Stop('No installed backup for this SAME iPod UUID. Nothing changed.')
    for idx,(folder,rec) in enumerate(folders[:10],1):print(f' {idx}. {folder.name} ({rec.get("status")})')
    choice=input('Choose number to restore [other cancels]: ').strip()
    if not choice.isdigit() or not 1<=int(choice)<=min(10,len(folders)):raise Stop('Cancelled.')
    folder,rec=folders[int(choice)-1]
    if rec['status']!='installed':
        print("WARNING: Earlier installation interrupted. Restore proceeds only if tracked files match the original or this kit's copy.")
    if input('Type RESTORE APPS to replace ONLY the 14 tracked paths with their pre-install state: ').strip()!='RESTORE APPS':raise Stop('Cancelled.')
    if info_for(vol)['uuid']!=device['uuid']:raise Stop('Device changed. Refusing.')
    restored=restore_files(vol,folder,rec,verify_current=True)
    rec['status']='restored';save_receipt(folder,rec)
    print('SUCCESS. Restored the exact pre-install condition of',len(restored),'tracked paths.')
    print('Other /Apps data, music, firmware, and IconState.plist not touched.')

def self_test(m):
    with tempfile.TemporaryDirectory(prefix='nano7-kit-test-') as t:
        root=Path(t)/'iPod';root.mkdir()
        (root/'iPod_Control'/'Device').mkdir(parents=True)
        # Original pre-existing custom file must be restored, new ones must vanish.
        original=root/'Apps'/'Executables'/'Chess.hbapp'
        original.parent.mkdir(parents=True)
        original.write_bytes(b'old-app-binary')
        device={'uuid':'SELFTEST-DEVICE','size':15_700_000_000,'filesystem':'HFS+','disk':'SIM','name':'SIM'}
        global DEST
        prior=DEST; DEST=Path(t)/'backups'
        try:
            folder,rec=backup(root,device,m)
            assert rec['original_files']['Apps/Executables/Chess.hbapp']['existed']
            put_files(root,m)
            for rel,meta in m['files'].items():
                assert digest(root/rel)==meta['sha256'],rel
            restore_files(root,folder,rec,verify_current=True)
            assert original.read_bytes()==b'old-app-binary'
            for rel in m['files']:
                if rel!='Apps/Executables/Chess.hbapp':assert not (root/rel).exists(),rel
            # Simulate interruption halfway through an install, then restore.
            partial_dir,partial_rec=backup(root,device,m)
            for rel in sorted(m['files'])[:4]:
                dst=secure_target(root,safe_rel(rel))
                ensure_parent(root,safe_rel(rel))
                atomic_copy(PAYLOAD/rel,dst)
            restore_files(root,partial_dir,partial_rec,verify_current=True)
            assert original.read_bytes()==b'old-app-binary'
            for rel in m['files']:
                if rel!='Apps/Executables/Chess.hbapp':assert not (root/rel).exists(),rel
            # Symlink trap must be detected.
            (root/'Apps'/'Icons').rmdir()
            (root/'Apps'/'Icons').symlink_to(Path(t))
            try:secure_target(root,Path('Apps/Icons/Chess.bin'))
            except Stop:pass
            else:raise AssertionError('Symlink escape protection failed')
        finally:DEST=prior
    print('PASS: Payload hashes, install, full readback, rollback, and symlink protection.')

def menu():
    m=verify_payload()
    while True:
        print('\n'+('='*56))
        print('iPod nano 7G — Community Mac Kit 1.0 (2012 / 2015)')
        print('='*56)
        print('1  Inspect nano (READ ONLY)')
        print('2  Install four apps (REQUIRES existing compatible untether)')
        print('3  Verify installed files (READ ONLY)')
        print('4  Restore this kit\'s previous install')
        print('5  Offline package self-test (NO device needed)')
        print('6  Open setup/compatibility guide')
        print('Q  Quit')
        choice=input('Select option: ').strip().upper()
        if choice=='Q':return
        try:
            if choice=='5':self_test(m);continue
            if choice=='6':
                print('Read START-HERE.md, 2012-AND-2015-GUIDE.md and TROUBLESHOOTING.md in this folder.')
                continue
            if choice not in ('1','2','3','4'):print('Unknown option.');continue
            vol,dev=detect();show_header(vol,dev)
            if choice=='1':print('READ-ONLY INSPECTION COMPLETE. Firmware patch and precise 2012/2015 revision cannot be detected from mount data.')
            elif choice=='2':install(vol,dev,m,select_year())
            elif choice=='3':verify(vol,dev,m)
            elif choice=='4':restore_menu(vol,dev)
        except (Stop,OSError,ValueError) as e:print('\nSTOP:',e)
        except Exception as e:
            print('\nUNEXPECTED ERROR:',type(e).__name__,str(e))
            traceback.print_exc()
        input('\nPress Return for menu...')

if __name__=='__main__':
    try:
        m=verify_payload()
        if len(sys.argv)>1 and sys.argv[1]=='--self-test':self_test(m)
        elif len(sys.argv)>1:raise Stop('Unknown argument; use menu or --self-test.')
        else:menu()
    except Stop as e:
        print('STOP:',e,file=sys.stderr);sys.exit(1)
