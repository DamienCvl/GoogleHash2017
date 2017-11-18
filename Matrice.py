class Matrice:

    def __init__(self): # le tableau = une liste de liste
        self.matrice = [[]]

        self.rows = -1
        self.columns = -1
        self.routerRange = -1
        self.backboneCost = -1
        self.routerCost = -1
        self.budget = -1
        self.backboneInit = []
    def setLine(self): # ajout d une liste pour representer une nouvelle ligne
        self.matrice.append([])

    def setPoint(self,line,objet): # ajout d un objet sur la ligne = line
        self.matrice[line].append(objet)

    def getPoint(self,x,y): #getPoint(45,60) retournera l'objet de la ligne 45 colonne 60
        return self.matrice[x][y]
