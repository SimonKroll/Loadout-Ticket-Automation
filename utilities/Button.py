import RPi.GPIO as GPIO
import time

class ButtonHandler:
    def __init__(self, button_pin, waitout_time_seconds, pressed_function):
        self.button_pin = button_pin
        self.wait_time_seconds = waitout_time_seconds
        self.pressed_function = pressed_function
        self.last_press_time = 0

        # Set up GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Set up the event handler
        GPIO.add_event_detect(self.button_pin, GPIO.FALLING, callback=self.button_pressed, bouncetime=300)

    def button_pressed(self, channel):
        current_time = time.time()

        if current_time - self.last_press_time >= self.wait_time_seconds:
            self.pressed_function()
        else:
            print(f"Wait for {self.wait_time_seconds} seconds before pressing again.")

        self.last_press_time = current_time

    def run(self):
        try:
            while True:
                # Your main loop logic goes here
                time.sleep(0.1)  # Optional: Adjust sleep time based on your needs

        except KeyboardInterrupt:
            pass

        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    # Your more complicated function
    def my_complex_function():
        # Replace this with your actual function
        print("Button pressed!")

    # Create an instance of ButtonHandler
    button_handler = ButtonHandler(button_pin=17, wait_time_seconds=30, complex_function=my_complex_function)
    button_handler.run()
