import Point

class Target(Point):

    def __init__(self):
        super.__init__()
        self.isCovered = False #Etat de la cible : True si couverte, False sinon
        