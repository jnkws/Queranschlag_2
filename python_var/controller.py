import numpy as np
import cv2
from sklearn.cluster import DBSCAN
import line_detection
import terminal
import matplotlib.pyplot as plt



if __name__ == "__main__":
    imgRaw = cv2.imread(r'python_var\data\testp57.png')
    lines = line_detection.LineDetection(imgRaw)
    data = lines.getDrawableData()
    plt.plot(data[0], data[1], "rp")
    plt.show()