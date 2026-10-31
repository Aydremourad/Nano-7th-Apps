# Stock nano setup — 2012 and 2015

You need compatible untethered firmware before installing the four apps. This is the part that depends on the nano revision.

**Never flash 2012 firmware on a 2015 nano, or vice versa.**

## Suggested to Back up before changing firmware (unless you can easily get music and info back)

Keep a full device image if you have a way to make one. A file backup isn't a firmware backup, and neither can guarantee recovery from a bad firmware write.

## Download the firmware

Unzip [Nano7-Mac-Apps-1.1.zip](Nano7-Mac-Apps-1.1.zip?raw=1) into Downloads. In Terminal:

```bash
bash ~/Downloads/Nano7-Mac-Apps/Get-Firmware.command
```

Choose **2012** or **2015**. The tool downloads the matching published `ipod_sun_untethered` v1.0 IPSW and checks its SHA-256 and file size. It only saves the file in `~/Downloads/Nano7-Firmware` — it doesn't write to the iPod.

You can also get the files yourself from [the upstream release](https://github.com/nfzerox/ipod_sun_untethered/releases/tag/1.0).

## Getting patched firmware onto the nano

The [original NanoApps guide](https://github.com/nfzerox/NanoApps#getting-started) documents installing the patched firmware through **Windows iTunes**, then using **Linux** (or a Raspberry Pi) for its app installer. That's the published route for new installs.

On a Mac, Finder or iTunes can select an IPSW with **Option + Check for Update**, as described in [ipod_theme](https://github.com/nfzerox/ipod_theme). An end-to-end Mac-only installation of this particular untethered firmware hasn't been validated for this kit, so it may not work on every macOS version or nano. Don't mistake an IPSW being downloaded for a completed patch. 

For DFU/firmware flashing or recovery on macOS, see [LeUnBrIck](https://github.com/LycanLD/LeUnBrIck); it lists both 2012 and 2015 nano 7G support, but it's a separate tool and hasn't been tested with this four-app pack. Don't mix different flashing methods in one attempt.

**Already patched, but Finder causes reboots?** The NanoApps untether can conflict with iTunes/Finder while connected. Try connecting in Disk Mode to copy app files: restart by holding Home + Sleep/Wake, then immediately hold both volume buttons as the screen goes dark. The README covers this.

## Install the apps

After you know compatible untethered firmware is running and the nano mounts:

```bash
bash ~/Downloads/Nano7-Mac-Apps/Start.command
```

Choose **1** to inspect, **5** to test files, then **2** to install. Safely eject and test each app.

**For 2012 nanos:** this ZIP's A/B resident loader came from a 2015 setup and hasn't been hardware-tested completely on 2012. If you can't recover a nonbooting device, use the upstream [NanoApps](https://github.com/nfzerox/NanoApps) installation method rather than this custom loader. This is very rarely needed. Usually you can just restore the nano if something goes wrong but it is here in case.

## Problems?

- Installer can't see the nano: disconnect other iPods, use a genuine cable, and check it's mounted in disk utility. Also to get into dfu, a usbc lightning will not work. You need usba and a dongle for modern macs. 
- No new icons: open Music and return Home. If they're still missing, check your firmware and loader combination. In addition, you must restart every time you load new icons or else changes won't show. 
- Undo app changes: reattach a mountable nano and choose **4** in the installer. Only the tracked files can be restored.
