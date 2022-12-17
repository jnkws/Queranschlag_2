import time
import os
from picamera2 import Picamera2, Preview
# GPIO-Bibliothek laden
import RPi.GPIO as GPIO

class Camera:
    def __init__(self) -> None:
        # BCM-Nummerierung verwenden
        GPIO.setmode(GPIO.BCM)

        # GPIO 17 (Pin 11) als Ausgang setzen
        GPIO.setup(17, GPIO.OUT)
        # GPIO 17 (Pin 11) auf LOW setzen
        GPIO.output(17, False)
        self.picam2 = Picamera2()
        self.config = self.picam2.create_still_configuration(main={"size": (3280, 2464), })
        self.picam2.configure(self.config)

    def captureImg(self):
        GPIO.output(17, True)   
        self.picam2.start()
        time.sleep(2)

        self.picam2.capture_file(f'img_raw.png')
        GPIO.output(17, False)
        

    def __del__(self):
        GPIO.cleanup()