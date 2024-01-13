import RPi.GPIO as GPIO
from time import sleep 

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