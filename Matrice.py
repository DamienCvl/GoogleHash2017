from Point import Point

class Matrice:

    def __init__(self):
        self.matrice = []

        self.rows = -1
        self.columns = -1
        self.routerRange = -1
        self.backboneCost = -1
        self.routerCost = -1
        self.budget = -1
        self.backboneInit = []

    def inialisation(self):
        for i in range(self.rows):
            self.matrice.append([0] * self.columns) #Ajoute 10 lignes de 10 entiers(int) ayant pour valeurs 0

    def setPoint(self, line, column, objet): # ajout d un objet a la suite de la 'column'
        self.matrice[line][column] = objet

    def getPoint(self, line, column): #getPoint(45,60) retournera l'objet de la ligne 45 colonne 60
        return self.matrice[line][column]

    def toString(self):
        print(self.rows)
        print(self.columns)
        for ligne in range(self.rows):
            for colonne in range(self.columns):
                print(self.matrice[ligne][colonne].typePoint, end='')
            print()
