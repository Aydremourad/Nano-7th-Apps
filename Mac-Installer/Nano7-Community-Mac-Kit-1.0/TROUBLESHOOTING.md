# Troubleshooting — Mac, iPod nano 7G 2012/2015

**Problem: `python3: command not found`.** Install Python 3 for macOS from https://www.python.org/downloads/macos/ and restart Terminal. On your Mac, `python3 --version` must return Python 3.8+ (3.9+ recommended). No `pip install` required.

**Problem: `.command` says permission denied.** Run `bash /path/to/Start.command` in Terminal instead of double-clicking; to get the path, drag the file into Terminal. The installer does not need `sudo`. macOS may show an unsigned developer warning; review the script before choosing to open it.

**Problem: "Exactly ONE mounted ... iPod is required."** Connect a single **7th-gen** nano using a data-capable Lightning cable. Unlock and allow it to mount normally. Confirm `iPod_Control` exists in the device volume. Disconnect all other iPods. A device in DFU/recovery cannot be mounted as a normal data volume, and this script intentionally cannot run there. If macOS doesn't detect it, try a direct USB port, different cable, or inspect System Information → USB.

**Problem: volume is the correct nano but the installer refuses/removable check fails.** This is a deliberate guard. Do not replace checks or run with `sudo`. Record `diskutil info -plist "/Volumes/your-iPod-name"` and ask the community for assistance **after redacting your serial/UUID**.

**Problem: installed files verify but no icons appear.** File copying alone does not prove homebrew firmware or startup-hook compatibility. Confirm you really have a **working untethered 7G firmware** with the appropriate startup system. Open Music and go back Home to refresh. If using the upstream NanoApps resident approach, follow that project's `Install resident only` instructions; it is not the same as this custom A/B loader and the formats must not be mixed blindly.

**Problem: icons appear but an app crashes.** First recheck kit menu option 3. Make a note of exactly which app, your nano's revision, and which homebrew firmware and loader you had. On 2012 hardware, this exact custom loader is not physically tested. Stop using the crashing app. Use kit menu option 4 to restore the prior 14 files; never guess a firmware flash as a fix.

**Problem: icons vanish after reboot.** The patched startup hook may not be installed or may not recognize this A/B loader. The upstream NanoApps `./start` often requires re-registration after restart, while another tested untethered approach can auto-start its resident. Confirm which path you actually use. Restoring the app files will not undo a separate firmware modification.

**Problem: Finder/iTunes causes reboot loop.** A known interaction with the upstream modified SCSI channel. Disconnect from Finder sync, use upstream-documented Disk Mode for media syncing and avoid attempting to fix it with repeated firmware restores.

**Problem: installation interrupted.** If the script itself reports an error, it attempts rollback using its Desktop backup. Look in `~/Desktop/Nano7-App-Backups/` and preserve that folder. If it cannot roll back, do NOT install over the top or delete any existing custom files. Seek advice with a redacted log before retrying.

**Problem: option 4 won't restore because some files changed.** Other tools changed the app pack since the backup. This kit refuses to overwrite the new changes. Preserve both sets and ask for manual comparison. Do not delete the backup folder.

**Problem: iPod is bootlooping or in DFU.** A mismatched startup payload can cause a boot loop even though the installer did not flash firmware. If the volume cannot mount, this kit cannot roll back the files. This kit is a file installer, not a repair or recovery utility. A stock restore may erase all personal content and may be dangerous if mixed with the wrong revision. Consult your *specific* firmware project's recovery procedure. Firmware modifications can cause a permanent brick.

**Useful diagnostics for Discord:** device revision (2012/2015 and evidence), firmware version *and* source of patched build, filesystem (HFS+ or FAT), Intel/Apple Silicon Mac, exact menu option and its text, whether a backup was made, whether icons appear and survive a cold reboot. **Never post serial numbers, disk UUIDs, passwords, personal notes, or full backups.**
