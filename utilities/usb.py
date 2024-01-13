#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep 
import os
import logging    # first of all import the module
import sys

logging.basicConfig(filename='/home/pi/dev/Loadout-Ticket-Automation/utilities/log.txt', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning(os.getcwd())

if len(sys.argv) > 1:
    drive_name = sys.argv[1]
    logging.warning(f"USB drive {drive_name} inserted. Running Python script...")

    drive_path = f"/dev/{drive_name}"  # Assuming the drive is mounted under /dev

    mount_path = "/home/pi/dev/Loadout-Ticket-Automation/usbmount"

    # mount the drive
    os.system(f"mount {drive_path} {mount_path}")

    # For Testing
    f = open(mount_path+"/instructions.txt", "a")
    f.write("Now the file has more content! yayaya\n")
    f.close()

    #TODO: check for file and read it into DB
    #
    #

    #TODO: write out current DB state and instruction files
    #
    #

    #TODO: umount usb
    #
    #


print(GPIO.getmode())

buzzer = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT) 

GPIO.output(buzzer,1)
sleep(0.125)
GPIO.output(buzzer,0)
sleep(0.125)
GPIO.output(buzzer,1)
sleep(0.125)
GPIO.output(buzzer,0)


GPIO.cleanup()
