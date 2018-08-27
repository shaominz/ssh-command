import time
import logging

logging.basicConfig(level = "DEBUG")

count = 1;
while True:
    print("xxxxxxxxxxxxx %s" % count)
    logging.info("xxxxxxxxxxxxx %s" % count)
    count = count + 1
    time.sleep(1)
    
    