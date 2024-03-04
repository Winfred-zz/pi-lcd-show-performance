import lcddriver
from time import *
lcd = lcddriver.lcd()
lcd.lcd_clear()
import subprocess
import psutil

# This script will display the status of the raid array, in use memory and CPU load on the lcd screen.
# The LCD has two lines, so the script will display the raid status on the first line and the memory and CPU load on the second line. 
# The script will run in an infinite loop, updating the status every 60 seconds. 
# The script will use the mdadm command to get the raid status and psutil to get the memory and CPU load. 

while True:
    output = subprocess.check_output(['mdadm', '-D', '/dev/md0'])
    output = output.decode('utf-8').split("\n")
    # get the line that has the state:
    for line in output:
        if "State :" in line:
            state = line.strip()
            break
    mem = psutil.virtual_memory()
    lcd.lcd_clear()
    lcd.lcd_display_string(state, 1)
    lcd.lcd_display_string("Mem:" + str(int(mem.percent)) + "% CPU:" + str(int(psutil.cpu_percent())) + "%", 2)
    sleep(60)
