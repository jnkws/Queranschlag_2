import numpy as np
import cv2
from sklearn.cluster import DBSCAN
import param_server
import line

class LineDetection:
    def __init__(self, src) -> None:
        self.img = src
        self.imageProcessing()
        self.findLines()

    def imageProcessing(self):
        self.gray = self.rgb2gray(self.img)
        self.treshADA = self.tresholdAdaptive(self.gray)
        self.morphImg = self.morphologicalOperations(self.treshADA)
        self.imgProcd = self.custom1DFilter(self.morphImg)

    def findLines(self):
        self.pixelCoordinates = self.getPixelCoordinates(self.imgProcd)
        self.labels, self.nClusters, self.nNoise, self.uniqueLabels = self.clusterData(self.pixelCoordinates)
        self.lines = []
        for noCluster in range(self.nClusters):
            edges = self.getClusterEdges(self.labels,\
                                            self.pixelCoordinates,\
                                            noCluster)
            self.lines.append(line.Line(edges))
        self.nLines = self.nClusters
        self.lines.sort(key= lambda x : x.lineCoeff, reverse=True)
        
        
   

    def rgb2gray(self, src):
        return cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    def tresholdAdaptive(self, src):
        return cv2.adaptiveThreshold(src, 1,\
             param_server.adaptiveMethod,\
             param_server.thresholdType,\
             param_server.blockSize,\
             param_server.c)

    def morphologicalOperations(self, src):
        return cv2.morphologyEx(src,\
             param_server.morphType,\
             param_server.kernel)

    def custom1DFilter(self, src):

        return cv2.filter2D(src, -1, param_server.filterKernel)

    def getPixelCoordinates(self, src):
        """Search the pixel which could be a line and store the coordinates.

        Args:
            src (np.ndarray): Binary image array

        Returns:
            list: Coordinates of possible line pixel [[x, ...], [y, ...]]
        """
        #test = np.where(src==0)
        #pixelCoordinates = [0,0]
        pixelCoordinates = list(np.where(src == 0))
        #Change columns
        pixelCoordinates[0], pixelCoordinates[1] = \
            pixelCoordinates[1], pixelCoordinates[0]
        #Change Coordinates in "normal" Coordinationssystem
        size = len(pixelCoordinates[1])
        pixelCoordinates[1] = pixelCoordinates[1] * (-1) + size
        return pixelCoordinates

    def clusterData(self, src):
        """Cluster Data with DBSCAN

        Args:
            src (list): Coordiantes from samples in a list with shape [[x, ...], [y, ...]]

        Returns:
            np.array(): labels
            int: Number of clusters
            int: Number of noise points
            set: Possible labels
        """
        data = np.stack((src[0], src[1]), axis=-1) #Convert [[x, ...], [y, ...]] in [[x1,y1], ...,[xn,yn]]
        db = DBSCAN(eps=param_server.maxDistance, min_samples=param_server.minSamples).fit(data)
        labels = db.labels_
        nClusters = len(set(labels)) - (1 if -1 in labels else 0)
        nNoise = list(labels).count(-1)
        uniqueLabels = set(labels)
        return labels, nClusters, nNoise, uniqueLabels

    def getClusterEdges(self, labels, pixelCoordinates, noLabel):
        """Take a cluster and compute the edge point

        Args:
            labels (ndarray): _description_
            pixelCoordinates (list): _description_
            noLabel (int): _description_

        Returns:
            array: edges
        """
        edges = np.array([[-1,-1],[-1,-1],[-1,-1],[-1,-1]])
        indices = np.where(labels == noLabel)[0]
        for index in indices:
            point_x = pixelCoordinates[0][index]
            point_y = pixelCoordinates[1][index]

            if point_x > edges[0][0] or edges[0][0] == -1:
                edges[0][0] = point_x
                edges[0][1] = point_y
            if point_x < edges[2][0] or edges[2][0] == -1:
                edges[2][0] = point_x
                edges[2][1] = point_y
            if point_y > edges[1][1] or edges[1][1] == -1:
                edges[1][0] = point_x
                edges[1][1] = point_y
            if point_y < edges[3][1] or edges[3][1] == -1:
                edges[3][0] = point_x
                edges[3][1] = point_y
        return edges

    def getDrawableData(self):
        dataX = []
        dataY = []
        for line in self.lines:
            dataX.append(line.getDrawableData()[0])
            dataY.append(line.getDrawableData()[1])
        return dataX, dataY

    def getCuttingPoint(self, lineSide):
        if "left" == lineSide:
            return self.lines[0].getLeftBorder()
        elif "right" == lineSide:
            return self.lines[0].getRightBorder()
        else:
            return (self.lines[0].getLeftBorder()\
                 + self.lines[0].getRightBorder())/2

           



