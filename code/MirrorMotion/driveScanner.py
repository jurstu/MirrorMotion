import subprocess
import json
from LoggingSetup import getLogger
from threading import Thread
import time
from Signals import Signal

logger = getLogger(__name__)



class DriveScanner:
    def __init__(self):
        self.connectSignal = Signal("new drive connected")
        self.disconnectSignal = Signal("drive got disconnected")

        self.interestingDrives = self.scan()


    def scan(self):

        
        while(1):
            try:
                output = subprocess.check_output(['lsblk', '--json'])
                drives = json.loads(output)

                interestingDrives = {}

                for key, value in drives.items():
                    for dev in value:
                        if(dev['type'] == "disk"):
                            for child in dev["children"]:
                                interestingDrives[child["name"]] = child

                return interestingDrives
            except:
                time.sleep(0.001)

    def doSinglePass(self):
        interestingDrives = self.scan()

        for key in interestingDrives:
            
            if not key in self.interestingDrives  or (interestingDrives[key] != self.interestingDrives[key]):
                if(interestingDrives[key]["mountpoints"][0] is not None):
                    logger.info(f"connected {key} at {interestingDrives[key]["mountpoints"]}")
                #self.connectSignal.trigger()


        # backward - detecting disconnections
        for key in self.interestingDrives:
            if not key in interestingDrives:
                logger.info(f"disconnected {key}")
                self.disconnectSignal.trigger([key])

        self.interestingDrives = interestingDrives
    
    def startThread(self):
        self.t = Thread(target=self.loop, daemon=True)
        self.t.start()

    def loop(self):

        while(1):
            self.scan()
            self.doSinglePass()
            time.sleep(0.02)




