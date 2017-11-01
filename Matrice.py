class Matrice:
    
    def __init__(self):
        self.matrice = [[]]
        
    def setLine(self):
        self.matrice.append([])
        
    def setPoint(self,line,objet):
        self.matrice[line].append(objet)
        
    def getPoint(self,x,y):
        return self.matrice[x][y]
