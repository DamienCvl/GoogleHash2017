from Point import Point

class Wall(Point):
    def __init__(self, posX, posY):
        Point.__init__(self,"#",posX, posY)



    #comportement d un Wall a definir
    def getType(self): #retourne le type, 0 pour Target, 1 pour Wall, 2 pour Void
        return 1
