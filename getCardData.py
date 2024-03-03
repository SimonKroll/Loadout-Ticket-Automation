from mfrc522 import SimpleMFRC522
from utilities import Buzzer, encoder
from time import sleep



buzzer = Buzzer()
reader = SimpleMFRC522()

try:
        while True:
                id, text = reader.read()

                print(f"ID is: {id}")
                print(f"encoded ID is:\n ===== {encoder.id_encode(id)} =====\n")
                print(text)
                buzzer.beep()
finally:
        pass