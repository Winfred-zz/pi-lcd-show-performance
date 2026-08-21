# pi-lcd-show-performance

This is a continuation of either this:

https://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/

or this guide:

https://tutorials-raspberrypi.com/control-a-raspberry-pi-hd44780-lcd-display-via-i2c/

Once you have followed these guides, you will have a working hd44780 LCD that is connected to a Raspberry Pi.

i2c_lib.py and lcddriver.py are the commonly available and used libraries.

lcdshowstatus.py will display the current memory % usage and CPU percentage usage, along with the mdadm RAID state.

Instead of a `@reboot` cronjob, it runs as a systemd service so it's automatically restarted if it ever crashes.

## Deploying

Updates are pushed straight from git — no manual file copying. One-time setup on the Pi:

```
scp deploy/setup-pi.sh pi@<pi-host>:~/
ssh pi@<pi-host> sh setup-pi.sh
```

That creates a bare repo at `/opt/pi-lcd-show-performance.git` with a `post-receive` hook, and grants your Pi account passwordless `sudo` to restart just this one service. Follow the printed instructions to add the Pi as a git remote, push once to populate `/opt/pi-lcd-show-performance`, then install the systemd unit (see `deploy/setup-pi.sh` for the exact command).

After that, every deploy is just:

```
git push pi main
```

which checks out the new code into `/opt/pi-lcd-show-performance` and restarts `lcdshowstatus.service`.

Logs are written to `/var/log/lcdshowstatus.log`; check `journalctl -u lcdshowstatus` for service-level (start/stop/restart) events.

To check the service status: `sudo systemctl status lcdshowstatus.service`

To see the latest logs: `tail -f /var/log/lcdshowstatus.log`

[See here for more details](https://winfred.com/projects/pi-lcd-show-performance/)

<!-- test commit: verifying attribution settings -->