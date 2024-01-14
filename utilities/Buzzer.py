# Buzzer.py
import RPi.GPIO as GPIO
import time

class Buzzer:
    def __init__(self, pin=27):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.pin = pin

    def beep(self, repetitions=1, duration=0.5, pause=0.1):
        for _ in range(repetitions):
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(duration)
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(pause)

# Clean up GPIO when the program ends
def _cleanup():
    GPIO.cleanup()

# Run cleanup when the script ends or is interrupted
import atexit
atexit.register(_cleanup)

if __name__ == "__main__":
    buzzer = Buzzer()
    buzzer.beep()
