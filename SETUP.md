# Stock nano setup — 2012 and 2015

You need compatible untethered firmware before installing the four apps. This is the part that depends on the nano revision.

## Which one?

The 2015 nano was offered in gold; if yours is gold it's the 2015 version. Other colors can overlap. If you don't know when it was made, check its history before you touch firmware. Both versions can show A1446 and 1.1.2 — those aren't enough to identify the revision.

**Never flash 2012 firmware on a 2015 nano, or vice versa.**

## Back up before changing firmware

Copy your media and other files off the iPod first. Keep a full device image if you have a way to make one. A file backup isn't a firmware backup, and neither can guarantee recovery from a bad firmware write.

## Download the firmware

Unzip [Nano7-Mac-Apps-1.1.zip](Nano7-Mac-Apps-1.1.zip?raw=1) into Downloads. In Terminal:

```bash
bash ~/Downloads/Nano7-Mac-Apps/Get-Firmware.command
```

Choose **2012** or **2015**. The tool downloads the matching published `ipod_sun_untethered` v1.0 IPSW and checks its SHA-256 and file size. It only saves the file in `~/Downloads/Nano7-Firmware` — it doesn't write to the iPod.

You can also get the files yourself from [the upstream release](https://github.com/nfzerox/ipod_sun_untethered/releases/tag/1.0).

## Getting patched firmware onto the nano

The [original NanoApps guide](https://github.com/nfzerox/NanoApps#getting-started) documents installing the patched firmware through **Windows iTunes**, then using **Linux** (or a Raspberry Pi) for its app installer. That's the published route for new installs.

On a Mac, Finder or iTunes can select an IPSW with **Option + Check for Update**, as described in [ipod_theme](https://github.com/nfzerox/ipod_theme). An end-to-end Mac-only installation of this particular untethered firmware hasn't been validated for this kit, so it may not work on every macOS version or nano. Don't mistake an IPSW being downloaded for a completed patch. Firmware flashing can permanently brick the nano.

For DFU/firmware flashing or recovery on macOS, see [LeUnBrIck](https://github.com/LycanLD/LeUnBrIck); it lists both 2012 and 2015 nano 7G support, but it's a separate tool and hasn't been tested with this four-app pack. Don't mix different flashing methods in one attempt.

**Already patched, but Finder causes reboots?** The NanoApps untether can conflict with iTunes/Finder while connected. Try connecting in Disk Mode to copy app files: restart by holding Home + Sleep/Wake, then immediately hold both volume buttons as the screen goes dark. The NanoApps README covers this.

## Install the apps

After you know compatible untethered firmware is running and the nano mounts:

```bash
bash ~/Downloads/Nano7-Mac-Apps/Start.command
```

Choose **1** to inspect, **5** to test files, then **2** to install. Safely eject and test each app.

**For 2012 nanos:** this ZIP's A/B resident loader came from a 2015 setup and hasn't been hardware-tested on 2012. If you can't recover a nonbooting device, use the upstream [NanoApps](https://github.com/nfzerox/NanoApps) installation method rather than this custom loader.

## Problems?

- Installer can't see the nano: disconnect other iPods, use a good cable, and check it's mounted with `iPod_Control/Device`.
- No new icons: open Music and return Home. If they're still missing, check your firmware and loader combination.
- Undo app changes: reattach a mountable nano and choose **4** in the installer. Only the tracked files can be restored.
- Nano doesn't boot: stop repeated flash attempts. Read [upstream recovery notes](https://github.com/olievans123/nano7-untethered/blob/main/untether/docs/RECOVERY.md) or [LeUnBrIck](https://github.com/LycanLD/LeUnBrIck). A full recovery isn't guaranteed.
