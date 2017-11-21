from Void import Void
from Wall import Wall
from Target import Target
from Matrice import Matrice
from Point import Point
import math
import time

def lectureFichier(path):
    lineNumber = 0 # Numero de la ligne
    rowCount = 0 # Nombre de ligne
    matrice = Matrice()
    with open(path) as f: # On ouvre le fichier et on traite ligne par ligne
        for line in f:
            #On split les Vertical dans les 3 premiers cas pour recuperer toutes les informations nécessaires tel
            #que le budget, le rayon, le cout, etc...
            if(lineNumber == 0):
                line1 = line.split()
                matrice.rows = int(line1[0])
                matrice.columns = int(line1[1])
                matrice.routerRange = int(line1[2])
                matrice.inialisation()
            elif(lineNumber == 1):
                line2 = line.split()
                matrice.backboneCost = int(line2[0])
                matrice.routerCost = int(line2[1])
                matrice.budget = int(line2[2])
            elif(lineNumber == 2):
                line3 = line.split()
                matrice.backboneInit = (int(line3[0]),int(line3[1]))
            else:
                columnCount = 0
                for char in line: #Pour chaque char dans la ligne, on le traite en fonction de ce qu'il est
                    #print("Ligne {} | Colonne : {}".format(rowCount, columnCount))
                    if char == '-': #Si c'est un tiret un crée un void
                        matrice.setPoint(rowCount, columnCount, Point("-"))
                    elif char == '#': #si c'est un hashtag on crée un wall
                        matrice.setPoint(rowCount, columnCount, Point("#")) #Sinon si c'est un point on crée un target
                    elif char == '.':
                        matrice.setPoint(rowCount, columnCount, Target())
                    columnCount += 1 #On incrémente le nombre de colonne
                rowCount += 1 #On incrémente le nombre de ligne
                #matrice.setLine()
            lineNumber += 1 #On incrémente le numéro de ligne
    #matrice.toString()
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
     for compteurLignes in range(matrice.rows):
         for compteurColonnes in range(matrice.columns):
             if(cptRouteurs<(matrice.budget // matrice.routerCost)):
                 if compteurDeTarget < (matrice.routerRange*2) and not (matrice.getPoint(compteurLignes,compteurColonnes).typePoint == "-" or matrice.getPoint(compteurLignes,compteurColonnes).typePoint == "#"):
                    if not matrice.getPoint(compteurLignes,compteurColonnes).isCovered :
                        compteurDeTarget = compteurDeTarget + 1 #incrément de la zone à couvrir

                    elif compteurDeTarget !=0: #Dans le cas où il y a des zones difficiles d'accès
                        matrice.getPoint(compteurLignes,compteurColonnes  - (compteurDeTarget // 2)).isRouter = True #Le point devient Router (Juste pour le visuel)
                        routers.append([compteurLignes, compteurColonnes - (compteurDeTarget // 2)]) # On pose le router au centre de la zone et la rajoute dans la liste de routers
                        covering(matrice,matrice.routerRange,compteurLignes,compteurColonnes  - (compteurDeTarget // 2)) # On change les cellules concernées en Covered
                        compteurDeTarget = 0 #Réinialisation de la taille de la zone
                        cptRouteurs +=1

                 else:
                    if compteurDeTarget != 0:
                        matrice.getPoint(compteurLignes,compteurColonnes  - (compteurDeTarget // 2)).isRouter = True
                        routers.append([compteurLignes, compteurColonnes - (compteurDeTarget // 2)]) # On pose le router au centre de la zone et la rajoute dans la liste de routers
                        covering(matrice,matrice.routerRange,compteurLignes,compteurColonnes  - (compteurDeTarget // 2))# On change les cellules concernées en Covered
                        cptRouteurs +=1
                    compteurDeTarget = 0
     print(cptRouteurs)
     return matrice,routers

def ecrireFichier(router = [], backbone = [], cables = []):

    filename = "output" + time.strftime("%d_%m_%y__%H_%M") + ".txt"

    f = open("output/" + filename,'a')

    retourChar = "\n"

    if (backbone != []):
        line = "backbone : [" + str(backbone[0]) + ";" + str(backbone[1]) + "]\n"
    else: line = "backbone : n/a\n"
    f.writelines(line)

    f.writelines(retourChar)

    if (router != []):
        for i in range(len(router)):
            line = "routeur " + str(i+1) + " : [" + str(router[i][0]) + ";" + str(router[i][1]) + "]\n"
            f.writelines(line)
    else:
        f.writelines("router : n/a\n")

    f.writelines(retourChar)

    if (cables != []):
        for i in range(len(cables)):
            line = "cables " + str(i+1) + " : [" + str(cables[i][0]) + ";" + str(cables[i][1]) + "]\n"
            f.writelines(line)
    else:
        f.writelines("cables : n/a\n")

    f.close()


def calculPoids(murs, target, multDistance = 100, multCoverage = 100):

    for case in target:
        distances = []
        for mur in murs:
            dist = math.sqrt((case[0] - mur [0])**2 + (case[1] - mur [1])**2)
            distances.append(dist)

        if (case.isCovered):
            couverture = multCoverage
        else:
            couverture = 0
        poids = (min(distances) * multDistance) / (1 + couverture)
        case.weight = poids







if __name__ == '__main__':

    mat=lectureFichier("maps/charleston_road.in")
    mat,routeurs=positionnerRouteur(mat)
    #print(routeurs)
    '''for compteurLignes in range(mat.rows):
         for compteurColonnes in range(mat.columns):
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
