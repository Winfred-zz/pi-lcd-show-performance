import logging
import subprocess
from time import sleep

import lcddriver
import psutil

# This script will display the status of the raid array, in use memory and CPU load on the lcd screen.
# The LCD has two lines, so the script will display the raid status on the first line and the memory and CPU load on the second line.
# The script will run in an infinite loop, updating the status every 60 seconds.
# The script will use the mdadm command to get the raid status and psutil to get the memory and CPU load.

logging.basicConfig(
    filename='/var/log/lcdshowstatus.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
)
logger = logging.getLogger(__name__)


def get_raid_state():
    """Return the mdadm State line, or a fallback string if it can't be read."""
    try:
        output = subprocess.check_output(['mdadm', '-D', '/dev/md0'], stderr=subprocess.STDOUT)
        output = output.decode('utf-8').split("\n")
        for line in output:
            if "State :" in line:
                return line.strip()
        logger.warning("mdadm output had no 'State :' line: %r", output)
    except (subprocess.CalledProcessError, FileNotFoundError, OSError) as exc:
        logger.error("Failed to read raid state: %s", exc)
    return "State: unknown"


def main():
    lcd = lcddriver.lcd()
    lcd.lcd_clear()
    logger.info("lcdshowstatus started")
    while True:
        state = get_raid_state()
        mem = psutil.virtual_memory()
        lcd.lcd_clear()
        lcd.lcd_display_string(state, 1)
        lcd.lcd_display_string("Mem:" + str(int(mem.percent)) + "% CPU:" + str(int(psutil.cpu_percent())) + "%", 2)
        sleep(60)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception("lcdshowstatus crashed")
        raise
