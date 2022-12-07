class Line:
    def __init__(self, edges) -> None:
        self.x0 = edges[0,0]
        self.y0 = edges[0,1]
        self.x1 = edges[1,0]
        self.y1 = edges[1,1]
        self.x2 = edges[2,0]
        self.y2 = edges[2,1]
        self.x3 = edges[3,0]
        self.y3 = edges[3,1] 

        self.length = self.calcDistance(self.y1, self.y3)
        self.width  = self.calcDistance(self.x0, self.x2)

        self.lineCoeff = self.length / self.width

        self.grade = -1 #Ranking of all detected lines


    #Variablein ParaServer ide festlegt ob rechte oder linke Seite des Clusters genommen wird
    def calcDistance(self, val1, val2):
        return abs(val1 - val2)
  
    def getDrawableData(self):
        x = [self.x0,self.x1,self.x2,self.x3]
        y = [self.y0,self.y1,self.y2,self.y3]
        return x, y

   