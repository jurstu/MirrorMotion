from MirrorMotion import DriveScanner
import time




ds = DriveScanner()
ds.startThread()

while(1):
    time.sleep(1)