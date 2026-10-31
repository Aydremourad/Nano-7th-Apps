# Nano 7th Apps

Calculator, Contacts, Chess and Golf for the iPod nano 7th generation. Mac installer and app files are in one ZIP.

**[Download the Mac kit](Nano7-Mac-Apps-1.1.zip?raw=1)**

## Already have homebrew firmware?

1. Download the ZIP and unzip it in **Downloads**.
2. Connect one nano to the Mac.
3. Open Terminal and run:

```bash
bash ~/Downloads/Nano7-Mac-Apps/Start.command
```

Choose **1** to check your nano, **5** to check the files, then **2** to install. Follow the prompts and safely eject when it finishes. Opening Music and going back Home should refresh the icons.

The installer needs Python 3 (`python3 --version`). [Download Python for Mac](https://www.python.org/downloads/macos/) if you don't have it.

## Still on stock firmware?

Read **[Stock nano setup](SETUP.md)** before running the app installer. The ZIP also has `Get-Firmware.command` for downloading and checking the correct **2012 or 2015** firmware. It doesn't flash your nano.

The 2012 and 2015 nanos use different patched firmware, even though both may be labelled A1446. Make sure you know which one you have.

## A few things to know

- This four-app pack came from a working **2015 nano**. The included resident loader hasn't been verified on a 2012 nano, so don't treat it as a tested 2012 installer.
- Your nano needs **compatible untethered firmware** before the app install. This kit doesn't jailbreak a stock nano.
- The installer backs up the 14 files it replaces on your Desktop and has a restore option (**4**) if the nano still mounts. It's not a full-device or firmware backup.
- The installation and rollback were tested offline. Other devices and firmware variants still need real-world testing.

If you want the whole homebrew app collection, use [NanoApps](https://github.com/nfzerox/NanoApps) instead of installing its loader over this pack.

[Stock setup, both revisions](SETUP.md) · [Credits and licenses](LICENSES.md)

ZIP SHA-256: `b5d9bce82d855e662a9a8a275e67b8fb5646167bbce1f03f120a61b08a0bb513`
