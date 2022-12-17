#!/usr/bin/python3

# Capture a PNG while still running in the preview mode.

import time
import os
from picamera2 import Picamera2, Preview
# GPIO-Bibliothek laden
import RPi.GPIO as GPIO

# BCM-Nummerierung verwenden
GPIO.setmode(GPIO.BCM)

# GPIO 17 (Pin 11) als Ausgang setzen
GPIO.setup(17, GPIO.OUT)
# GPIO 17 (Pin 11) auf LOW setzen
GPIO.output(17, False)

picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": (3280, 2464), })
picam2.configure(config)
#picam2.start_preview(Preview.QTGL)

#preview_config = picam2.create_preview_configuration(main={"size": (3280, 2464)})
#picam2.configure(preview_config)
dirs = os.listdir()
name = str(len(dirs)+1)
type(name)

GPIO.output(17, True)   
picam2.start()
time.sleep(2)

picam2.capture_file(f'testp{name}.png')
GPIO.output(17, False)

# Benutzte GPIOs freigeben
GPIO.cleanup()