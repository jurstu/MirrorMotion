import subprocess
import json
from LoggingSetup import getLogger


logger = getLogger(__name__)



class DriveScanner:
    def __init__(self):
        pass


    def scan(self):
        output = subprocess.check_output(['lsblk', '--json'])
        drives = json.loads(output)
        logger.info(drives)