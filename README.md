# pi-lcd-show-performance

This is a continuation of either this:

https://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/

or this guide:

https://tutorials-raspberrypi.com/control-a-raspberry-pi-hd44780-lcd-display-via-i2c/

Once you have followed these guides, you will have a working hd44780 LCD that is connected to a Raspberry Pi.

i2c_lib.py and lcddriver.py are the commonly available and used libraries.

lcdshowstatus.py can be scheduled with a cronjob and will display the current memory % usage and CPU percentage usage.