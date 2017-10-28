class Point:
    """ Class qui défini un point avec :
            - une coordonnée en x
            - une coordonnée en y
    """

    def __init__(self,x,y):
        self.x = x
        self.y = y


    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self,value):
        self.x = value

    def setY(self,value):
        self.y = value

    def getPosition(self):
        return (self.x,self.y)
