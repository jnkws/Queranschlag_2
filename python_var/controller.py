import numpy as np
import cv2
from sklearn.cluster import DBSCAN
import line_detection
#import g_code_sender
import matplotlib.pyplot as plt
import logging
import RPi.GPIO as GPIO
import take_pic
import g_code_sender
import param_server
import time

def gpioInitialization():
    # BCM-Nummerierung verwenden
    GPIO.setmode(GPIO.BCM)
    # GPIO 17 (Pin 11) als Ausgang setzen
    GPIO.setup(17, GPIO.OUT)
    # GPIO 17 (Pin 11) auf LOW setzen
    GPIO.output(17, False)
    GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)


if __name__ == "__main__":
    gpioInitialization()
    camera = take_pic.Camera()
    camera.captureImg()
    #logging.getLogger().setLevel(logging.INFO)
    imgRaw = cv2.imread(r'python_var\img_raw.png')
    lines = line_detection.LineDetection(imgRaw)
    data = lines.getDrawableData()
    #plt.plot(data[0], data[1], "rp")
    #plt.show()
   
    sender = g_code_sender.GCodeSender("COM8")
    value = "G01 F4000 X" + str(lines.getCuttingPoint(param_server.cuttingSide)) + "\n"
    sender.send(str.encode(value))

    time.sleep(5)

    sender.homePos()







    GPIO.cleanup()