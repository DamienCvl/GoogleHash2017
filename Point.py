class Point:
    #Classe Point qui est en réalité un type de point "#" pour le wall,"." pour la target et "-" pour le void
    def __init__(self, typePoint, posX=None, posY=None):
        self.typePoint = typePoint
        self.posX = posX
        self.posY = posY
