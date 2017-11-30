from Void import Void
from Wall import Wall
from Target import Target
from Matrice import Matrice
from Point import Point
from constante import Constante
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
                        mur = Point("#", rowCount, columnCount)
                        matrice.setPoint(rowCount, columnCount, mur)
                        matrice.wallList.append(mur)
                    elif char == '.':
                        target = Target(rowCount,columnCount)
                        matrice.setPoint(rowCount, columnCount, target)#Sinon si c'est un point on crée un target
                        matrice.targetList.append(target)
                    columnCount += 1 #On incrémente le nombre de colonne
                rowCount += 1 #On incrémente le nombre de ligne
                #matrice.setLine()
            lineNumber += 1 #On incrémente le numéro de ligne
    #matrice.toString()
    return matrice


def distance(xA, yA, xB, yB):

    dist = math.sqrt((xA - xB)**2 + (yA - yB)**2)
    return dist

def redWeight(target, x, y):
    dist = distance(target.posX, target.posY, x, y)
    mult = (Constante.MULTI_POIDS_NEIGH ** int(dist))
    target.weight = target.weight * mult



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
                target = matrice.getPoint(posLignes - i, posColonnes)
                target.isCovered = True
                redWeight(target, posLignes, posColonnes)



            if matrice.getPoint(posLignes - i, posColonnes).typePoint == "#": 
                murNord = True  
                rayonNord = i - 1

        if(not murEst):
            if matrice.getPoint(posLignes, posColonnes + i).typePoint == "-":
                pass
            if matrice.getPoint(posLignes, posColonnes + i).typePoint == ".":
                target = matrice.getPoint(posLignes, posColonnes + i)
                target.isCovered = True
                redWeight(target, posLignes, posColonnes)

            if matrice.getPoint(posLignes, posColonnes + i).typePoint == "#": 
                murEst = True
                rayonEst = i - 1

        if(not murSud):
            if matrice.getPoint(posLignes + i, posColonnes).typePoint == "-":
                pass
            if matrice.getPoint(posLignes + i, posColonnes).typePoint == ".":
                target = matrice.getPoint(posLignes + i, posColonnes)
                target.isCovered = True
                redWeight(target, posLignes, posColonnes)

            if matrice.getPoint(posLignes + i, posColonnes).typePoint == "#": 
                murSud = True
                rayonSud = i - 1

        if(not murOuest):
            if matrice.getPoint(posLignes, posColonnes - i).typePoint == "-":
                pass
            if matrice.getPoint(posLignes, posColonnes - i).typePoint == ".":
                target = matrice.getPoint(posLignes, posColonnes - i)
                target.isCovered = True
                redWeight(target, posLignes, posColonnes)

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

            if (matrice.getPoint(i, j).typePoint == "."):
                target = matrice.getPoint(i, j)
                target.isCovered = True
                redWeight(target, posLignes, posColonnes)

            elif matrice.getPoint(i, j).typePoint == "#":
                rayonE = posColonnes - j
                break

    #Est
    for j in range(posColonnes + 1, posColonnes + 1 + rayonEst, +1):
        for i in range(posLignes + 1, posLignes + 1 + rayonS, +1):

            if (matrice.getPoint(i, j).typePoint == "."):
                target = matrice.getPoint(i, j)
                target.isCovered = True
                redWeight(target, posLignes, posColonnes)

            elif matrice.getPoint(i, j).typePoint == "#":
                rayonS = i - posLignes
                break

    #Sud
    for i in range(posLignes + 1, posLignes + 1 + rayonSud, + 1):
        for j in range(posColonnes - 1, posColonnes - 1 - rayonO, -1):

            if (matrice.getPoint(i, j).typePoint == "."):
                target = matrice.getPoint(i, j)
                target.isCovered = True
                redWeight(target, posLignes, posColonnes)

            elif matrice.getPoint(i, j).typePoint == "#":
                #print("WALL")
                rayonO = j - posColonnes
                break

    #Ouest
    for j in range(posColonnes - 1, posColonnes - 1 - rayonOuest, -1):
        for i in range(posLignes - 1, posLignes - 1 - rayonN, -1):

            if (matrice.getPoint(i, j).typePoint == "."):
                target = matrice.getPoint(i, j)
                target.isCovered = True
                redWeight(target, posLignes, posColonnes)

            elif matrice.getPoint(i, j).typePoint == "#":
                rayonN = posLignes - i
                break

    matrice.getPoint(posLignes, posColonnes).isCovered = True
    matrice.getPoint(posLignes, posColonnes).weight *= Constante.MULTI_POIDS_NEIGH



def getMaxWeight(targetList):

    maxTarget = targetList[0]

    for target in targetList:
        if (target.weight > maxTarget.weight):
            maxTarget = target

    return maxTarget

def positionnerRouteur(matrice):
     routers = [] #liste des positions des routeurs
     cptRouteurs = 0

     calculPoids(matrice)

     placement = True

     # On prend le poids max et on place un routeur
     # On décrémente la zone environnante du routeur placé et on réitère

     while (placement):

         if (cptRouteurs < (matrice.budget // matrice.routerCost)):

             maxTarget = getMaxWeight(matrice.targetList)# target de poids maximal

             if ([maxTarget.posX,maxTarget.posY] not in routers):
                 routers.append([maxTarget.posX,maxTarget.posY])  # ajout du routeur
                 cptRouteurs += 1
                 maxTarget.isRouter = True
                 covering(matrice, matrice.routerRange, maxTarget.posX, maxTarget.posY)
                 #print(maxTarget.posX, maxTarget.posY, maxTarget.weight)
                 #print("nbrouter = ",cptRouteurs)
             else:
                 maxTarget.weight *= Constante.MULTI_POIDS_NEIGH

             # test si on continue de placer
             if (testCoverage(matrice.targetList) == 0):
                 placement = False
             else:
                 print(((len(matrice.targetList) - testCoverage(matrice.targetList)) / len(matrice.targetList)), " %")

         else:
             placement = False


     print("nbRouteurs = ", cptRouteurs)
     print("nbTargets = ", len(matrice.targetList))
     print("nbRouteursBudget = ", (matrice.budget // matrice.routerCost))
     return matrice,routers

def ecrireFichier(map, timeExec, router = [], backbone = [], cables = []):

    filename = "output" + time.strftime("%d_%m_%y__%H_%M") + ".txt"

    f = open("output/" + filename,'a')

    retourChar = "\n"

    line = "######"+time.strftime("%d_%m_%y__%H_%M")+"######"
    f.writelines(line)
    f.writelines(retourChar)
    line = "nombre routeurs = " + str(len(router))
    f.writelines(line)
    f.writelines(retourChar)
    line = "temps d'execution = " + str(timeExec)
    f.writelines(line)
    f.writelines(retourChar)

    for ligne in map:
        f.writelines(ligne)
        f.writelines(retourChar)

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


def calculPoids(matrice, multDistance = Constante.MULTI_POIDS_DISTANCE, multCoverage = Constante.MULTI_POIDS_COUVERTURE):
    tabPoids = []
    for target in matrice.targetList:
        distances = []
        for mur in matrice.wallList:
            dist = math.sqrt((target.posX - mur.posX)**2 + (target.posY - mur.posY)**2)
            distances.append(dist)

        if (target.isCovered):
            couverture = multCoverage
        else:
            couverture = 0

        poids = ((min(distances) * multDistance) / (1 + couverture))
        target.weight = poids #Plus le poids est grand mieux c'est

        print("x : " + str(target.posX) + " y : " + str(target.posY) + " a un poids de : " + str(target.weight))

def testCoverage(targetList):

    nonCouverts = 0
    for target in targetList:
        if(not target.isCovered):
            nonCouverts += 1
    return nonCouverts



def ecrireLog(logs):
    fichier = open("log.txt", "a")
    fichier.write(logs)
    fichier.close()


if __name__ == '__main__':

    start = time.time()
    #os.remove("log.txt")
    mat=lectureFichier("maps/rue_de_londres.in")
    mat,routeurs=positionnerRouteur(mat)
    #print(routeurs)
    map = []
    for compteurLignes in range(mat.rows):
         line = ""
         for compteurColonnes in range(mat.columns):
                if(mat.getPoint(compteurLignes,compteurColonnes).typePoint == "."):
                    if(mat.getPoint(compteurLignes,compteurColonnes).isCovered):
                        if mat.getPoint(compteurLignes,compteurColonnes).isRouter:
                            print("R",end='')
                            line += "R"
                        else:
                            print("-",end='')
                            line += "-"
                    else:
                        print("X",end='')
                        line += "X"
                elif(mat.getPoint(compteurLignes,compteurColonnes).typePoint == "#"):
                    print("#",end='')
                    line += "#"
                else:
                    print("_",end='')
                    line += "_"
         map.append(line)
         print()
    end = time.time()
    exec = end - start
    print("Executed smoothly in ", exec, " seconds")
    ecrireFichier(map, exec, routeurs)

