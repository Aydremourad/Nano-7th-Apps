# Troubleshooting

**Terminal says `python3: command not found`.** Install Python 3 from [python.org](https://www.python.org/downloads/macos/) and reopen Terminal. No pip packages needed.

**The `.command` file doesn't open.** Use the Terminal command in the README instead of double-clicking. If you moved the folder, type `bash ` and drag `Start.command` into Terminal. Never use `sudo` for this installer.

**The nano isn't detected.** Use a working data cable, connect only one iPod, and check that the nano is mounted as a normal volume. This tool does not work in DFU/recovery mode. Don't disable its device checks.

**Files installed but no new icons.** Check that you're actually on compatible untethered/homebrew firmware. On the nano, open Music and return Home. The file copy alone won't activate homebrew on stock firmware.

**An app crashes.** Verify copied files with menu option 3. Note which app, hardware revision, and firmware/loader you're using. If the device still mounts, menu option 4 can restore the previous app files.

**The icons disappear after a restart.** Your current firmware's resident registration/startup hook may not match the included A/B loader. If you're using upstream NanoApps, follow its own "Install resident only" instructions, not a mix of both launchers.

**The nano bootloops or won't mount.** The installer cannot restore files while it cannot mount the volume. Stop retrying random firmware/loader combinations. Follow the recovery instructions for the exact firmware you used; a restore may wipe the nano and flashing the wrong revision can permanently damage it.

**Restore refuses to run.** The installer avoids overwriting later changes by other tools. Keep the Desktop backup folder and compare manually rather than forcing a restore.

When asking for help, include the year/revision, firmware source, Mac version, and exact error text. Don't post serial numbers, disk UUIDs, or your backups.