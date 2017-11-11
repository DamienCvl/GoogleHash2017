from TypePoint import TypePoint

class Target(TypePoint):
    #La classe Target hérite de point en y rajoutant les attributs isCovered pour la connexion et isRouter pour passer une cellule en router.
    def __init__(self):
        TypePoint.__init__(self,".")
        self.isCovered = False #Etat de la cible : True si couverte, False sinon
        self.isRouter = False
        self.weight = 0
