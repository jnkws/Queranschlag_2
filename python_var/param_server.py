import cv2
import numpy as np


#Image processing

#Adaptive threshold
adaptiveMethod = cv2.ADAPTIVE_THRESH_MEAN_C
thresholdType = cv2.THRESH_BINARY
blockSize = 21 #Size of a pixel neighborhood that is used to calculate a threshold value for the pixel: 3, 5, 7, and so on.
c = 10
#Morphological operations
morphType = cv2.MORPH_OPEN
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
#Custom 1D Filter
filterKernel = np.ones(168)/178

#Clustering (DBSCAN)
maxDistance = 180
minSamples = 300


#GCodeSender

baudRate = 115200