import numpy as np
import cv2
from sklearn.cluster import DBSCAN
import line_detection
#import g_code_sender
import matplotlib.pyplot as plt
import logging

#G1 F100 X40

if __name__ == "__main__":
    #logging.getLogger().setLevel(logging.INFO)
    imgRaw = cv2.imread(r'python_var\data\testp57.png')
    lines = line_detection.LineDetection(imgRaw)
    data = lines.getDrawableData()
    plt.plot(data[0], data[1], "rp")
    plt.show()