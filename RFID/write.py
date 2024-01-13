import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep 

buzzer = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT) 

reader = SimpleMFRC522()

try:
        text = input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        GPIO.output(buzzer,1)
        sleep(0.125)
        GPIO.output(buzzer,0)
        sleep(0.125)
        GPIO.output(buzzer,1)
        sleep(0.125)
        GPIO.output(buzzer,0)
        print("Written")
finally:
        GPIO.cleanup()