# iPod nano 7G — Community Mac App Kit v1.0

**For 2012/2013 and 2015 seventh-generation iPod nanos (A1446).**

## Read this first — what this ZIP actually does

This is a **Mac file installer for a nano that ALREADY has compatible untethered homebrew firmware**. It includes four custom apps: **Calculator, Contacts, Chess, and Golf**, the corresponding icons, app-pack manifests, and an A/B startup loader captured from a working custom 2015 nano configuration.

**It is NOT a jailbreak and NOT a firmware installer.** Running it on a completely stock nano cannot magically enable apps. First-time firmware installation is a separate, riskier process; see `2012-AND-2015-GUIDE.md`.

| | 2012/2013 nano 7G | 2015 nano 7G |
|---|---|---|
| Hardware | Original 7G (including 2013 Space Gray) | Mid-2015 colour revision |
| Apple model marking | A1446 | A1446 |
| Firmware modification | Needs supported **2012** patch/build | Needs supported **2015** patch/build |
| Included four-app files | **Experimental on this revision**; physical test not confirmed | Captured from a working gold 2015 nano; not broadly validated |
| This ZIP can unlock stock firmware | **No** | **No** |

**Warning:** Replacing the startup loader on an already-patched nano can itself cause crashes or a boot loop if its firmware hook is incompatible. A file backup may not be reachable if the device no longer mounts. An incorrect firmware restore can permanently brick a nano. This kit deliberately does not perform, automate, or suggest silently attempting a firmware restore. The firmware path is not officially supported by Apple. There is no verified universal Mac-only, one-click initial firmware solution here.

## Five-minute Mac installation — only for already-untethered nanos

1. Download and unzip the ZIP. Keep the whole `Nano7-Community-Mac-Kit-1.0` folder together; do **not** copy only the `.command` file.
2. Charge the nano. Disconnect all other iPods. Make sure the nano is running normal home-screen mode and connected to the Mac by a reliable Lightning cable. **Do not open Finder's sync/restore screen or iTunes** on a patched nano; those connections can trigger a reboot loop.
3. On a Mac with Python 3 installed, open **Terminal** and run:

   ```bash
   bash ~/Downloads/Nano7-Community-Mac-Kit-1.0/Start.command
   ```

   Or right-click `Start.command` and choose **Open** if permitted by macOS. If the extracted folder is somewhere else, drag `Start.command` into Terminal after typing `bash `.
4. Choose **1 — Inspect nano**. Confirm the mounted iPod is the expected ~16 GB volume; inspect does not change anything. If it cannot identify exactly one iPod, do not try to defeat the safeguard.
5. Choose **5 — Offline package self-test** if you'd like to validate the files and local copy/rollback logic without touching the device.
6. Choose **2 — Install four apps**, select 2012 or 2015 correctly, and read the prompts. It requires an explicit confirmation that *compatible, already-working untethered firmware* is installed. Choose Cancel if that is not true.
7. Before touching device files, the installer makes a local verified backup of the exact 14 affected paths at `~/Desktop/Nano7-App-Backups/`. It copies the files to `/Apps` using temporary files + atomic rename, checks the SHA-256 of each file **read back from the iPod**, and puts the startup marker in place **last**.
8. When it reports success, eject the nano safely. On its screen, open Music and then return to Home to refresh the app layout. Test the four apps. If you have not seen the icons yet, read the troubleshooting guide. Don't assume that a copied file proves the firmware patch is running.

## Included menu features

- **1 Inspect:** mounted-volume identity, disk ID, capacity, filesystem; read-only.
- **2 Install:** backs up and replaces 14 app/loader files; no sudo, no firmware access, no music changes.
- **3 Verify:** re-reads all installed files and compares SHA-256; read-only.
- **4 Restore:** restores the 14 paths to their pre-install condition for the **same iPod volume UUID**. Refuses if the files have been changed since this installer ran, to avoid destroying newer work.
- **5 Offline self-test:** checks checksums, installation and rollback using a temporary simulated nano directory, not your iPod.
- **6 Guide:** points you to the written instructions.

## Requirements

- Apple Silicon or Intel Mac, with `python3` available (`python3 --version`). Python 3 is available from https://www.python.org/downloads/macos/ . This installer needs **no pip packages**.
- 2012 or 2015 nano 7G with a **working compatible untethered firmware startup hook** already installed. Stock firmware does not support this bundle.
- Healthy Lightning cable and enough free space on the Mac's Desktop for a local backup of overwritten app files.
- The mounted iPod must be detected by macOS as a removable external device of ~16 GB with `iPod_Control/Device` present. If yours is not detected, the installer will refuse rather than use arbitrary paths.

## What is and is not backed up

The installer only backs up the 14 exact paths it will change (existing manifests, startup loader files, executables, icons). **This is not a full backup of the nano**, so make a separate full-device image before any experimental firmware work. This ZIP does not write outside `/Apps`, delete `/iPod_Control`, modify `IconState.plist`, reformat the device, or touch the firmware partition.

**Compatibility with other app suites:** This is a **curated four-app pack**, not the entire official NanoApps collection. It overwrites `AllApps.pack`, `AllApps-B.pack`, and associated startup loader paths. Existing homebrew apps may disappear from the Home Screen until restored; do not mix different loader ecosystems without understanding them. A menu-driven rollback is supplied.

**Testing disclosure:** The included files were copied from a working customized **2015 gold nano** configuration and validated byte-for-byte in this kit. The installer was exercised with an offline simulated iPod, not a physical Mac-connected 2012/2015 test unit for this community release. In particular, the included exact A/B resident has **not been verified on a 2012 nano**. Treat 2012 installs as experimental and only attempt on a recoverable, fully backed-up, already-unlocked device.

Read `2012-AND-2015-GUIDE.md` before advising anyone with stock firmware.
