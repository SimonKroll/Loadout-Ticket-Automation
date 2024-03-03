import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep


buzzer = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT) 

reader = SimpleMFRC522()

try:
        while True:
                id, text = reader.read()
                print(id)
                print(text)
   
                GPIO.output(buzzer,1)
                sleep(0.25)
                GPIO.output(buzzer,0)
                sleep(2)
finally:
        GPIO.cleanup()
