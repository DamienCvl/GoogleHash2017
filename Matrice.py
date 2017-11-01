class Matrice:
    
    def __init__(self): # le tableau = une liste de liste
        self.matrice = [[]]
        
    def setLine(self): # ajout d une liste pour representer une nouvelle ligne
        self.matrice.append([])
        
    def setPoint(self,line,objet): # ajout d un objet a la suite de la 'line'
        self.matrice[line].append(objet)
        
    def getPoint(self,x,y): #getPoint(45,60) retournera l'objet de la ligne 45 colonne 60
        return self.matrice[x][y]
