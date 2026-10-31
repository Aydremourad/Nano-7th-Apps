# Nano 7th Apps — Mac installer

Calculator, Contacts, Chess and Golf for the 7th-generation iPod nano. The ZIP has the apps, icons, startup files and Mac installer all together.

## Install from a Mac

1. **[Download Nano7-Community-Mac-Kit-1.0.zip](Nano7-Community-Mac-Kit-1.0.zip?raw=1)** and unzip it in Downloads.
2. Connect **one** nano to your Mac.
3. Open Terminal and run:

   ```bash
   bash ~/Downloads/Nano7-Community-Mac-Kit-1.0/Start.command
   ```

4. Choose **1** to check the nano, **5** to check the package offline, then **2** to install. Read the confirmation on screen.
5. Eject the nano. Open Music, then go back to the Home Screen to refresh the icons.

If you extracted the folder somewhere else, type `bash ` in Terminal, drag `Start.command` into Terminal and press Return. The installer needs Python 3 (`python3 --version`); [get it here](https://www.python.org/downloads/macos/) if it's missing.

## IMPORTANT — firmware and model

The nano must already have compatible homebrew/untethered firmware. The Mac installer copies files under `/Apps`; it does not flash an IPSW.

- **2015 nano:** the four-app files came from a customized 2015 gold nano. 

Both revisions may say **A1446**, but their patched firmware images aren't interchangeable. See [2012](2012.md) or [2015](2015.md) instructions if you still have stock firmware.

## What the installer does

The installer backs up any of the 14 tracked files it replaces to `~/Desktop/Nano7-App-Backups/`, copies and verifies the new files, and has a restore option (**4**) if the iPod still mounts. This is **not** a full firmware backup. It doesn't touch your music or deliberately change partitions.

The package contains Calculator, Contacts, Chess, Golf, their icons, the app pack, A/B startup/resident files, and a Python installer. 

[2012 guide](2012.md) · [2015 guide](2015.md) · [Troubleshooting](TROUBLESHOOTING.md) · [Credits and licenses](CREDITS-AND-LICENSES.md)

Credit

ZIP SHA-256: `04fdfdea212696519caf897b7b1c07a2ea27aa540a9688e5193fa43519ae2168`

Apps build on [NanoApps](https://github.com/nfzerox/NanoApps); firmware/loader work builds on [ipod_sun_untethered](https://github.com/nfzerox/ipod_sun_untethered) and [nano7-untethered](https://github.com/olievans123/nano7-untethered). 
