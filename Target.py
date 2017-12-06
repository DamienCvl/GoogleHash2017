from Point import Point

class Target(Point):
    #La classe Target hérite de point en y rajoutant les attributs isCovered pour la connexion et isRouter pour passer une cellule en router.
    def __init__(self, posX, posY):
        Point.__init__(self,".",posX,posY)
        self.isCovered = False #Etat de la cible : True si couverte, False sinon
        self.isRouter = False
        self.weight = 0
        self.isCoveredForReal = False
