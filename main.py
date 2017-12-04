from Void import Void
from Wall import Wall
from Target import Target
from Matrice import Matrice
from Point import Point
import backbone_path/backbone as BB_path
import math
import time
import os

def lectureFichier(path):
    lineNumber = 0 # Numero de la ligne
    rowCount = 0 # Nombre de ligne
    wallList = []
    TargetList = []
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
                        matrice.setPoint(rowCount, columnCount, Point("#"))
                        matrice.wallList.append((rowCount,columnCount))
                    elif char == '.':
                        matrice.setPoint(rowCount, columnCount, Target())#Sinon si c'est un point on crée un target
                        matrice.targetList.append((rowCount,columnCount,Target()))
                    columnCount += 1 #On incrémente le nombre de colonne
                rowCount += 1 #On incrémente le nombre de ligne
                #matrice.setLine()
            lineNumber += 1 #On incrémente le numéro de ligne
    #matrice.toString()
    return matrice

def covering(matrice, rayon, posLignes, posColonnes):

    rayonNord = rayon
    rayonEst = rayon
    rayonSud = rayon
    rayonOuest = rayon

    murNord = False
    murEst = False
    murSud = False
    murOuest = False

    for i in range(1, rayon + 1):

        if(not murNord):
            if matrice.getPoint(posLignes - i, posColonnes).typePoint == "-":
                pass
            if matrice.getPoint(posLignes - i, posColonnes).typePoint == ".":
                matrice.getPoint(posLignes - i, posColonnes).isCovered = True

            if matrice.getPoint(posLignes - i, posColonnes).typePoint == "#":
                murNord = True
                rayonNord = i - 1

        if(not murEst):
            if matrice.getPoint(posLignes, posColonnes + i).typePoint == "-":
                pass
            if matrice.getPoint(posLignes, posColonnes + i).typePoint == ".":
                matrice.getPoint(posLignes, posColonnes + i).isCovered = True

            if matrice.getPoint(posLignes, posColonnes + i).typePoint == "#":
                murEst = True
                rayonEst = i - 1

        if(not murSud):
            if matrice.getPoint(posLignes + i, posColonnes).typePoint == "-":
                pass
            if matrice.getPoint(posLignes + i, posColonnes).typePoint == ".":
                matrice.getPoint(posLignes + i, posColonnes).isCovered = True

            if matrice.getPoint(posLignes + i, posColonnes).typePoint == "#":
                murSud = True
                rayonSud = i - 1

        if(not murOuest):
            if matrice.getPoint(posLignes, posColonnes - i).typePoint == "-":
                pass
            if matrice.getPoint(posLignes, posColonnes - i).typePoint == ".":
                matrice.getPoint(posLignes, posColonnes - i).isCovered = True

            if matrice.getPoint(posLignes, posColonnes - i).typePoint == "#":
                murOuest = True
                rayonOuest = i - 1

    rayonN = rayonNord
    rayonE = rayonEst
    rayonS = rayonSud
    rayonO = rayonOuest

    ecrireLog("\n{} - {} - {} - {} - {}".format(rayon, rayonN, rayonE, rayonS, rayonO))
    ecrireLog("\n{} - {}".format(posLignes + 1, posColonnes + 1))

    #Nord
    for i in range(posLignes - 1, posLignes - 1 - rayonNord, -1):
        for j in range(posColonnes + 1, posColonnes + 1 + rayonE, +1):

            if not matrice.getPoint(i, j).typePoint == "-" or not matrice.getPoint(i, j).typePoint == "#":
                matrice.getPoint(i, j).isCovered = True

            elif matrice.getPoint(i, j).typePoint == "#":
                rayonE = posColonnes - j
                break

    #Est
    for j in range(posColonnes + 1, posColonnes + 1 + rayonEst, +1):
        for i in range(posLignes + 1, posLignes + 1 + rayonS, +1):

            if not matrice.getPoint(i, j).typePoint == "-" or not matrice.getPoint(i, j).typePoint == "#":
                matrice.getPoint(i, j).isCovered = True

            elif matrice.getPoint(i, j).typePoint == "#":
                rayonS = i - posLignes
                break

    #Sud
    for i in range(posLignes + 1, posLignes + 1 + rayonSud, + 1):
        for j in range(posColonnes - 1, posColonnes - 1 - rayonO, -1):

            if not matrice.getPoint(i, j).typePoint == "-" or not matrice.getPoint(i, j).typePoint == "#":
                matrice.getPoint(i, j).isCovered = True

            elif matrice.getPoint(i, j).typePoint == "#":
                rayonO = j - posColonnes
                break

    #Ouest
    for j in range(posColonnes - 1, posColonnes - 1 - rayonOuest, -1):
        for i in range(posLignes - 1, posLignes - 1 - rayonN, -1):

            if not matrice.getPoint(i, j).typePoint == "-" or not matrice.getPoint(i, j).typePoint == "#":
                matrice.getPoint(i, j).isCovered = True

            elif matrice.getPoint(i, j).typePoint == "#":
                rayonN = posLignes - i
                break

    matrice.getPoint(posLignes, posColonnes).isCovered = True

def positionnerRouteur(matrice):
     compteurDeTarget = 0 #Permet de placer le router
     routers = [] #liste des positions des routeurs
     cptRouteurs = 0
     #calculPoids(matrice.wallList,matrice.targetList)
     for compteurLignes in range(matrice.rows):
         for compteurColonnes in range(matrice.columns):
             if(cptRouteurs < (matrice.budget // matrice.routerCost)):
                 if compteurDeTarget < (matrice.routerRange * 2) and not (matrice.getPoint(compteurLignes, compteurColonnes).typePoint == "-" or matrice.getPoint(compteurLignes, compteurColonnes).typePoint == "#"):
                    if not matrice.getPoint(compteurLignes,compteurColonnes).isCovered :
                        compteurDeTarget = compteurDeTarget + 1 #incrément de la zone à couvrir

                    elif compteurDeTarget !=0: #Dans le cas où il y a des zones difficiles d'accès
                        if compteurDeTarget == 1:
                            matrice.getPoint(compteurLignes, compteurColonnes  - 1).isRouter = True
                            routers.append([compteurLignes, compteurColonnes - 1]) # On pose le router au centre de la zone et la rajoute dans la liste de routers
                            ecrireLog("\n")
                            ecrireLog("Routeur : {} | CompteurLignes : {} | CompteurColonnes : {} | Compteur de Targets : {}".format(matrice.getPoint(compteurLignes, compteurColonnes - 1).typePoint, compteurLignes, compteurColonnes  - 1, 1))
                            covering(matrice, matrice.routerRange, compteurLignes, compteurColonnes  - 1)# On change les cellules concernées en Covered
                            cptRouteurs +=1
                        elif compteurDeTarget > 1:
                            matrice.getPoint(compteurLignes, compteurColonnes  - (compteurDeTarget // 2)).isRouter = True
                            routers.append([compteurLignes, compteurColonnes - (compteurDeTarget // 2)]) # On pose le router au centre de la zone et la rajoute dans la liste de routers
                            ecrireLog("\n")
                            ecrireLog("Routeur : {} | CompteurLignes : {} | CompteurColonnes : {} | Compteur de Targets : {}".format(matrice.getPoint(compteurLignes, compteurColonnes - (compteurDeTarget // 2)).typePoint, compteurLignes, compteurColonnes  - (compteurDeTarget // 2), compteurDeTarget // 2))
                            covering(matrice, matrice.routerRange, compteurLignes, compteurColonnes  - (compteurDeTarget // 2))# On change les cellules concernées en Covered
                            cptRouteurs +=1
                        compteurDeTarget = 0

                 else:
                    if compteurDeTarget == 1:
                        matrice.getPoint(compteurLignes, compteurColonnes  - 1).isRouter = True
                        routers.append([compteurLignes, compteurColonnes - 1]) # On pose le router au centre de la zone et la rajoute dans la liste de routers
                        ecrireLog("\n")
                        ecrireLog("Routeur : {} | CompteurLignes : {} | CompteurColonnes : {} | Compteur de Targets : {}".format(matrice.getPoint(compteurLignes, compteurColonnes - 1).typePoint, compteurLignes, compteurColonnes  - 1, 1))
                        covering(matrice, matrice.routerRange, compteurLignes, compteurColonnes  - 1)# On change les cellules concernées en Covered
                        cptRouteurs +=1
                    elif compteurDeTarget > 1:
                        matrice.getPoint(compteurLignes, compteurColonnes  - (compteurDeTarget // 2)).isRouter = True
                        routers.append([compteurLignes, compteurColonnes - (compteurDeTarget // 2)]) # On pose le router au centre de la zone et la rajoute dans la liste de routers
                        ecrireLog("\n")
                        ecrireLog("Routeur : {} | CompteurLignes : {} | CompteurColonnes : {} | Compteur de Targets : {}".format(matrice.getPoint(compteurLignes, compteurColonnes - (compteurDeTarget // 2)).typePoint, compteurLignes, compteurColonnes  - (compteurDeTarget // 2), compteurDeTarget // 2))
                        covering(matrice, matrice.routerRange, compteurLignes, compteurColonnes  - (compteurDeTarget // 2))# On change les cellules concernées en Covered
                        cptRouteurs +=1
                    compteurDeTarget = 0
     #print(cptRouteurs)
     return matrice,routers

def ecrireFichier(router = [], backbone = []):

    filename = "output" + time.strftime("%d_%m_%y__%H_%M") + ".txt"

    f = open("output/" + filename,'a')


    if (backbone != []):
        line =  str(len(backbone[])) + "\n"
        f.writelines(line)

        for b in backbone[]:
            line = str(b[0]) + " " + str(b[1]) + "\n"
            f.writelines(line)

    if (router != []):
        line =  str(len(router[])) + "\n"
        f.writelines(line)

        for b in router[]:
            line = str(b[0]) + " " + str(b[1]) + "\n"
            f.writelines(line)


    f.close()


def calculPoids(wall, target, multDistance = 100, multCoverage = 100):
    for case in target:
        print(1)
        distances = []
        for mur in wall:
            dist = math.sqrt((case[0] - mur[0])**2 + (case[1] - mur[1])**2)
            distances.append(dist)

        if (case[2].isCovered):
            couverture = multCoverage
        else:
            couverture = 0
        poids = (min(distances) * multDistance) / (1 + couverture)
        case[2].weight = poids #Plus le poids est grand mieu c'est
        print("x : " + str(case[0]) + " y : " + str(case[1]) + " à un poid de : " + str(poids))

def ecrireLog(logs):
    fichier = open("log.txt", "a")
    fichier.write(logs)
    fichier.close()


if __name__ == '__main__':
    os.remove("log.txt")
    mat=lectureFichier("maps/charleston_road.in")
    mat,routeurs=positionnerRouteur(mat)
    #print(routeurs)
    mat.backbones = BB_path.main(routeurs,mat.backboneInit)
    for compteurLignes in range(mat.rows):
         for compteurColonnes in range(mat.columns):
                if(mat.getPoint(compteurLignes,compteurColonnes).typePoint == "."):
                    if(mat.getPoint(compteurLignes,compteurColonnes).isCovered):
                        if mat.getPoint(compteurLignes,compteurColonnes).isRouter:
                            print("R",end='')
                        else:
                            print("-",end='')
                    else:
                        print("X",end='')
                elif(mat.getPoint(compteurLignes,compteurColonnes).typePoint == "#"):
                    print("#",end='')
                else:
                    print("_",end='')
         print()
    ecrireFichier(routeurs,backbones)
