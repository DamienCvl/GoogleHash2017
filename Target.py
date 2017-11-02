class Target:

    def __init__(self):
        self.isCovered = False #Etat de la cible : True si couverte, False sinon
    def getType(self): #retourne le type, 0 pour Target, 1 pour Wall, 2 pour Void
        return 0
