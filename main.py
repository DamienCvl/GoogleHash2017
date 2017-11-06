from Void import Void
from Wall import Wall
from Target import Target
from Matrice import Matrice
from Point import Point

def lectureFichier(path):
    lineNumber = 0
    rowCount = 0
    matrice = Matrice()
    with open(path) as f:
        for line in f:
            if(lineNumber == 0):
                line1 = line.split()
            elif(lineNumber == 1):
                line2 = line.split()
            elif(lineNumber == 2):
                line3 = line.split()
            else:
                columnCount = 0
                for char in line:
                    if char == '-':
                        matrice.setPoint(rowCount,Point("-"))
                    elif char == '#':
                        matrice.setPoint(rowCount,Point("#"))
                    elif char == '.':
                        matrice.setPoint(rowCount,Target("."))
                    columnCount += 1
                rowCount += 1
                matrice.setLine()
            lineNumber += 1

    rows = line1[0]
    columns = line1[1]
    routerRange = line1[2]

    backboneCost = line2[0]
    routerCost = line2[1]
    budget = line2[2]

    backboneInit = (line3[0],line3[1])

    return matrice

def covering(matrice, rayon, posX, posY):
     #parcours Ouest > Est afin de passer isCovered a True
     for i in range(posX - rayon, posX + rayon + 1):
         for j in range(posY - rayon, posY + rayon + 1):
             if not matrice.getPoint(i, j) == "-" or not matrice.getPoint(i, j) == "#":
                 matrice.getPoint(i, j).isCovered = True
             else:
                j = posY + rayon

    #parcours Nord > Sud afin de passer isCovered a True
     for b in range(posY - rayon, posY + rayon + 1):
         for a in range(posX - rayon, posX + rayon + 1):
             if not matrice.getPoint(a, b) == "-" or not matrice.getPoint(a, b) == "#":
                 matrice.getPoint(a, b).isCovered = True
             else:
                 a = posX + rayon

def positionnerRouteur(matrice):
     compteurDeTarget = 0 #Permet de placer le router
     routers = [] #liste des positions des routeurs
     cptRouteurs = 0
     for compteurLignes in range(240):
         for compteurColonnes in range(180):
             if(cptRouteurs<290):
                 if compteurDeTarget < 20 and not (matrice.getPoint(compteurLignes,compteurColonnes).typePoint == "-" or matrice.getPoint(compteurLignes,compteurColonnes).typePoint == "#"):
                    if not matrice.getPoint(compteurLignes,compteurColonnes).isCovered :
                        compteurDeTarget = compteurDeTarget + 1 #incrément de la zone à couvrir

                    elif compteurDeTarget !=0: #Dans le cas où il y a des zones difficiles d'accès
                        matrice.getPoint(compteurLignes,compteurColonnes  - (compteurDeTarget // 2)).isRouter = True #Le point devient Router (Juste pour le visuel)
                        routers.append([compteurLignes, compteurColonnes - (compteurDeTarget // 2)]) # On pose le router au centre de la zone et la rajoute dans la liste de routers
                        covering(matrice,10,compteurLignes,compteurColonnes  - (compteurDeTarget // 2)) # On change les cellules concernées en Covered
                        compteurDeTarget = 0 #Réinialisation de la taille de la zone
                        cptRouteurs +=1

                 else:
                    if compteurDeTarget != 0:
                        matrice.getPoint(compteurLignes,compteurColonnes  - (compteurDeTarget // 2)).isRouter = True
                        routers.append([compteurLignes, compteurColonnes - (compteurDeTarget // 2)]) # On pose le router au centre de la zone et la rajoute dans la liste de routers
                        covering(matrice,10,compteurLignes,compteurColonnes  - (compteurDeTarget // 2))# On change les cellules concernées en Covered
                        cptRouteurs +=1
                    compteurDeTarget = 0
     print(cptRouteurs)
     return matrice,routers

#Méthode a finir pour creer les fichiers out
def ecrireFichier(routers):
    print(0)
    print(len(routers))
    for i in (routers):
        print (str(i[0])+" "+str(i[1]))

if __name__ == '__main__':

    mat=lectureFichier("maps/charleston_road.in")
    mat,routeurs=positionnerRouteur(mat)
    #print(routeurs)
    '''for compteurLignes in range(240):
         for compteurColonnes in range(180):
                if(mat.getPoint(compteurLignes,compteurColonnes).typePoint == "."):
                    if(mat.getPoint(compteurLignes,compteurColonnes).isCovered):
                        if mat.getPoint(compteurLignes,compteurColonnes).isRouter:
                            #print("R",end='')
                        else:
                            #print("-",end='')
                    else:
                        #print("X",end='')
                elif(mat.getPoint(compteurLignes,compteurColonnes).typePoint == "#"):
                    #print("#",end='')
                else:
                    #print("_",end='')
         #print()'''
    ecrireFichier(routeurs)
