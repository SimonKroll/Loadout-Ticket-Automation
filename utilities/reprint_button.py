import RPi.GPIO as GPIO
#from . import Buzzer
import time
import os
from Buzzer import Buzzer

# set the report directory
report_folder_path = "/home/pi/dev/Loadout-Ticket-Automation/output_files/reports"

buzzer = Buzzer()

# Set up the GPIO pin
BUTTON_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Assuming a pull-up resistor

# Callback function to handle the button press
def button_pressed_callback(channel):
    buzzer.beep(repetitions=1)
    time.sleep(0.25)
    if GPIO.input(channel) == GPIO.LOW:
        buzzer.beep(repetitions=3)
        # identify the most recent report file
        report_files = os.listdir(report_folder_path)
        report_files.sort(reverse=True)
        if report_files:
            file_path = os.path.join(report_folder_path, report_files[0])
            os.system(f"lp -d HP_Officejet_Pro_8600 {file_path}")





# Add an interrupt for a falling edge (button press)
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed_callback, bouncetime=5000)

try:
    print("Reprint button listener started")
    # Keep the script running to listen for button press
    while True:
        time.sleep(0.1)  # Reduce CPU usage
except KeyboardInterrupt:
    print("Exiting gracefully")
finally:
    GPIO.cleanup()  # Clean up on exit
