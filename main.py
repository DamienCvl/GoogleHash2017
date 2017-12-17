from Void import Void
from Wall import Wall
from Target import Target
from Matrice import Matrice
from Point import Point
from backbone_path import BB_search
import math
import time
import os
import math

def lectureFichier(path):
    lineNumber = 0 # Numero de la ligne
    rowCount = 0 # Nombre de ligne
    wallList = []
    TargetList = []
    matrice = Matrice()
    with open(path) as f: # On ouvre le fichier et on traite ligne par ligne
        for line in f:
            columnListTarget=[]
            columnListWall=[]
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
                        columnListWall.append(columnCount)
                    elif char == '.':
                        matrice.setPoint(rowCount, columnCount, Target())#Sinon si c'est un point on crée un target
                        matrice.targetList.append((rowCount,columnCount,Target()))
                        columnListTarget.append(columnCount)
                    columnCount += 1 #On incrémente le nombre de colonne
                if columnListWall:
                    matrice.wallList2[rowCount]=columnListWall
                if columnListTarget:
                    matrice.targetList2[rowCount]=columnListTarget
                rowCount += 1 #On incrémente le nombre de ligne
                #matrice.setLine()
            lineNumber += 1 #On incrémente le numéro de ligne
    #matrice.toString()
    return matrice

#Fonction de couverture autour des routeurs
def covering(matrice, rayon, posLignes, posColonnes):
    
    #Création de 4 variables permettant de retenir la taille maximal des rayons possibles sur les cardinalités
    rayonNord = rayon
    rayonEst = rayon
    rayonSud = rayon
    rayonOuest = rayon
    
    #Création de 4 variables booléennes permettant de retenir si un mur a été croisé ou non sur les cardinalités
    murNord = False
    murEst = False
    murSud = False
    murOuest = False

    #Boucle permettant d'itérer sur la taille du rayon
    for i in range(1, rayon + 1):
        #Si un mur n'a pas été croisé au Nord du Router
        if(not murNord):
            #Si le point étudié est un Void
            if matrice.getPoint(posLignes - i, posColonnes).typePoint == "-":
                #Ne rien faire
                pass
            #Si le point étudié est une Target
            if matrice.getPoint(posLignes - i, posColonnes).typePoint == ".":
                #Passer la Target en état Covered
                matrice.getPoint(posLignes - i, posColonnes).isCovered = True
            #Si le point étudié est un Wall
            if matrice.getPoint(posLignes - i, posColonnes).typePoint == "#":
                #Passer la variable <murCardinalité> à True
                murNord = True
                #Réduire la taille du rayon associé à la cardinalité
                rayonNord = i - 1
                
        #Si un mur n'a pas été croisé a l'Est du Router
        if(not murEst):
            if matrice.getPoint(posLignes, posColonnes + i).typePoint == "-":
                pass
            #Si le point étudié est une Target
            if matrice.getPoint(posLignes, posColonnes + i).typePoint == ".":
                #Passer la Target en état Covered
                matrice.getPoint(posLignes, posColonnes + i).isCovered = True
            #Si le point étudié est un Wall
            if matrice.getPoint(posLignes, posColonnes + i).typePoint == "#":
                #Passer la variable <murCardinalité> à True
                murEst = True
                #Réduire la taille du rayon associé à la cardinalité
                rayonEst = i - 1
                
        #Si un mur n'a pas été croisé au Sud du Router
        if(not murSud):
            if matrice.getPoint(posLignes + i, posColonnes).typePoint == "-":
                pass
            #Si le point étudié est une Target
            if matrice.getPoint(posLignes + i, posColonnes).typePoint == ".":
                #Passer la Target en état Covered
                matrice.getPoint(posLignes + i, posColonnes).isCovered = True
            #Si le point étudié est un Wall
            if matrice.getPoint(posLignes + i, posColonnes).typePoint == "#":
                #Passer la variable <murCardinalité> à True
                murSud = True
                #Réduire la taille du rayon associé à la cardinalité
                rayonSud = i - 1
                
        #Si un mur n'a pas été croisé a l'Ouest du Router
        if(not murOuest):
            if matrice.getPoint(posLignes, posColonnes - i).typePoint == "-":
                pass
            #Si le point étudié est une Target
            if matrice.getPoint(posLignes, posColonnes - i).typePoint == ".":
                #Passer la Target en état Covered
                matrice.getPoint(posLignes, posColonnes - i).isCovered = True
            #Si le point étudié est un Wall
            if matrice.getPoint(posLignes, posColonnes - i).typePoint == "#":
                #Passer la variable <murCardinalité> à True
                murOuest = True
                #Réduire la taille du rayon associé à la cardinalité
                rayonOuest = i - 1

#Creation de nouvelles variables reprenant la taille des nouveaux rayons
    rayonN = rayonNord
    rayonE = rayonEst
    rayonS = rayonSud
    rayonO = rayonOuest

    #Boucle permettant d'itérer sur la taille du nouveau rayon Nord en ligne 
    for i in range(posLignes - 1, posLignes - 1 - rayonNord, -1):
        #Boucle permettant d'itérer sur la taille du nouveau rayon Est en colonne
        for j in range(posColonnes + 1, posColonnes + 1 + rayonE, +1):
            #Si le point étudié, n'est ni un Void, ni un Wall
            if not matrice.getPoint(i, j).typePoint == "-" and not matrice.getPoint(i, j).typePoint == "#":
                #Passer la Target en état Covered
                matrice.getPoint(i, j).isCovered = True
            #Sinon, si le point est un Wall
            elif matrice.getPoint(i, j).typePoint == "#":
                #Réduire la taille du rayon Est
                rayonE = j - posColonnes
                #Arrêt de la boucle
                break

    #Boucle permettant d'itérer sur la taille du nouveau rayon Est en ligne 
    for j in range(posColonnes + 1, posColonnes + 1 + rayonEst, +1):
        #Boucle permettant d'itérer sur la taille du nouveau rayon Sud en colonne
        for i in range(posLignes + 1, posLignes + 1 + rayonS, +1):
            #Si le point étudié, n'est ni un Void, ni un Wall
            if not matrice.getPoint(i, j).typePoint == "-" and not matrice.getPoint(i, j).typePoint == "#":
                #Passer la Target en état Covered
                matrice.getPoint(i, j).isCovered = True
            #Sinon, si le point est un Wall
            elif matrice.getPoint(i, j).typePoint == "#":
                #Réduire la taille du rayon Sud
                rayonS = i - posLignes
                #Arrêt de la boucle
                break

    #Boucle permettant d'itérer sur la taille du nouveau rayon Sud en ligne 
    for i in range(posLignes + 1, posLignes + 1 + rayonSud, + 1):
        #Boucle permettant d'itérer sur la taille du nouveau rayon Ouest en colonne
        for j in range(posColonnes - 1, posColonnes - 1 - rayonO, -1):
            #Si le point étudié, n'est ni un Void, ni un Wall
            if not matrice.getPoint(i, j).typePoint == "-" and not matrice.getPoint(i, j).typePoint == "#":
                #Passer la Target en état Covered
                matrice.getPoint(i, j).isCovered = True
            #Sinon, si le point est un Wall
            elif matrice.getPoint(i, j).typePoint == "#":
                #Réduire la taille du rayon Ouest
                rayonO = posColonnes - j - 1
                #Arrêt de la boucle
                break

    #Boucle permettant d'itérer sur la taille du nouveau rayon Est en ligne 
    for j in range(posColonnes - 1, posColonnes - 1 - rayonOuest, -1):
        #Boucle permettant d'itérer sur la taille du nouveau rayon Nord en colonne
        for i in range(posLignes - 1, posLignes - 1 - rayonN, -1):
            #Si le point étudié, n'est ni un Void, ni un Wall
            if not matrice.getPoint(i, j).typePoint == "-" and not matrice.getPoint(i, j).typePoint == "#":
                #Passer la Target en état Covered
                matrice.getPoint(i, j).isCovered = True
            #Sinon, si le point est un Wall
            elif matrice.getPoint(i, j).typePoint == "#":
                #Réduire la taille du rayon Nord
                rayonN = posLignes - i - 1
                #Arrêt de la boucle
                break
            
    #Une fois que toutes les boucles sont finies, le Target correspondante au routeur passe en état Covered
    matrice.getPoint(posLignes, posColonnes).isCovered = True
    
#Meme méthode que covering cependant celle-ci gère les dictionnaires de targets en transferant les cellules couvertes dans le dictionnaire de wall
def covering2(matrice, rayon, posLignes, posColonnes):

    rayonNord = rayon
    rayonEst = rayon
    rayonSud = rayon
    rayonOuest = rayon

    murNord = False
    murEst = False
    murSud = False
    murOuest = False

    for i in range(1, rayon+1):
        if(not murNord):
            if matrice.getPoint(posLignes - i, posColonnes).typePoint == "-":
                pass
            if matrice.getPoint(posLignes - i, posColonnes).typePoint == ".":
                matrice.getPoint(posLignes - i, posColonnes).isCovered = True
                if posLignes - i in matrice.wallList2:
                    matrice.wallList2[posLignes - i].append(posColonnes)
                else:
                    matrice.wallList2[posLignes - i]=[posColonnes]
                if(posColonnes in matrice.targetList2[posLignes - i]):
                    matrice.targetList2[posLignes - i].remove(posColonnes)

            if matrice.getPoint(posLignes - i, posColonnes).typePoint == "#":
                murNord = True
                rayonNord = i

        if(not murEst):
            if matrice.getPoint(posLignes, posColonnes + i).typePoint == "-":
                pass
            if matrice.getPoint(posLignes, posColonnes + i).typePoint == ".":
                matrice.getPoint(posLignes, posColonnes + i).isCovered = True
                if posLignes in matrice.wallList2:
                    matrice.wallList2[posLignes].append(posColonnes + i)
                else:
                    matrice.wallList2[posLignes]=[posColonnes + i]
                if(posColonnes + i in matrice.targetList2[posLignes]):
                    matrice.targetList2[posLignes].remove(posColonnes + i)

            if matrice.getPoint(posLignes, posColonnes + i).typePoint == "#":
                murEst = True
                rayonEst = i

        if(not murSud):
            if matrice.getPoint(posLignes + i, posColonnes).typePoint == "-":
                pass
            if matrice.getPoint(posLignes + i, posColonnes).typePoint == ".":
                matrice.getPoint(posLignes + i, posColonnes).isCovered = True
                if posLignes + i in matrice.wallList2:
                    matrice.wallList2[posLignes + i].append(posColonnes)
                else:
                    matrice.wallList2[posLignes + i]=[posColonnes]
                if(posColonnes in matrice.targetList2[posLignes + i]):
                    matrice.targetList2[posLignes + i].remove(posColonnes)

            if matrice.getPoint(posLignes + i, posColonnes).typePoint == "#":
                murSud = True
                rayonSud = i

        if(not murOuest):
            if matrice.getPoint(posLignes, posColonnes - i).typePoint == "-":
                pass
            if matrice.getPoint(posLignes, posColonnes - i).typePoint == ".":
                matrice.getPoint(posLignes, posColonnes - i).isCovered = True
                if posLignes in matrice.wallList2:
                    matrice.wallList2[posLignes].append(posColonnes - i)
                else:
                    matrice.wallList2[posLignes]=[posColonnes - i]
                if(posColonnes - i in matrice.targetList2[posLignes]):
                    matrice.targetList2[posLignes].remove(posColonnes - i)


            if matrice.getPoint(posLignes, posColonnes - i).typePoint == "#":
                murOuest = True
                rayonOuest = i

    rayonN = rayonNord
    rayonE = rayonEst
    rayonS = rayonSud
    rayonO = rayonOuest


    #Nord
    for i in range(posLignes- 1, posLignes - 1 - rayonNord, -1):
        for j in range(posColonnes + 1, posColonnes + 1+  rayonE, +1):

            if not matrice.getPoint(i, j).typePoint == "-" and not matrice.getPoint(i, j).typePoint == "#":
                matrice.getPoint(i, j).isCovered = True
                if i in matrice.wallList2:
                    matrice.wallList2[i].append(j)
                else:
                    matrice.wallList2[i]=[j]
                if(j in matrice.targetList2[i]):
                    matrice.targetList2[i].remove(j)

            elif matrice.getPoint(i, j).typePoint == "#":
                rayonE = j - posColonnes
                break

    #Est
    for j in range(posColonnes + 1 , posColonnes + 1 + rayonEst, +1):
        for i in range(posLignes + 1, posLignes + 1 + rayonS, +1):

            if not matrice.getPoint(i, j).typePoint == "-" and not matrice.getPoint(i, j).typePoint == "#":
                matrice.getPoint(i, j).isCovered = True
                if i in matrice.wallList2:
                    matrice.wallList2[i].append(j)
                else:
                    matrice.wallList2[i]=[j]

                if(j in matrice.targetList2[i]):
                    matrice.targetList2[i].remove(j)

            elif matrice.getPoint(i, j).typePoint == "#":
                rayonS = i - posLignes
                break

    #Sud
    for i in range(posLignes + 1, posLignes + 1 + rayonSud, + 1):
        for j in range(posColonnes - 1, posColonnes -1 - rayonO, -1):

            if not matrice.getPoint(i, j).typePoint == "-" and not matrice.getPoint(i, j).typePoint == "#":
                matrice.getPoint(i, j).isCovered = True
                if i in matrice.wallList2:
                    matrice.wallList2[i].append(j)
                else:
                    matrice.wallList2[i]=[j]
                if(j in matrice.targetList2[i]):
                    matrice.targetList2[i].remove(j)

            elif matrice.getPoint(i, j).typePoint == "#":
                rayonO = posColonnes - j - 1
                break

    #Ouest
    for j in range(posColonnes - 1, posColonnes - 1 - rayonOuest, -1):
        for i in range(posLignes - 1, posLignes - 1 - rayonN, -1):

            if not matrice.getPoint(i, j).typePoint == "-" and not matrice.getPoint(i, j).typePoint == "#":
                matrice.getPoint(i, j).isCovered = True
                if i in matrice.wallList2:
                    matrice.wallList2[i].append(j)
                else:
                    matrice.wallList2[i]=[j]
                if(j in matrice.targetList2[i]):
                    matrice.targetList2[i].remove(j)

            elif matrice.getPoint(i, j).typePoint == "#":
                rayonN = posLignes - i - 1
                break


    matrice.getPoint(posLignes, posColonnes).isCovered = True
    if posLignes in matrice.wallList2:
        matrice.wallList2[posLignes].append(posColonnes)
    else:
        matrice.wallList2[posLignes]=[posColonnes]
    if(posColonnes in matrice.targetList2[posLignes]):

        matrice.targetList2[posLignes].remove(posColonnes)

#Meme principe que covering excepté que l'on ne change pas les cellules, on se contente de calculer le nombre de cellules qui peuvent être couvertes
def coveringScore(matrice, rayon, posLignes, posColonnes):

    rayonNord = rayon
    rayonEst = rayon
    rayonSud = rayon
    rayonOuest = rayon
    score = 0
    murNord = False
    murEst = False
    murSud = False
    murOuest = False

    for i in range(1, rayon+1):
        if(not murNord):
            if matrice.getPoint(posLignes - i, posColonnes).typePoint == "-":
                pass
            if matrice.getPoint(posLignes - i, posColonnes).typePoint == ".":
                if not matrice.getPoint(posLignes - i, posColonnes).isCovered:
                    score+=1

            if matrice.getPoint(posLignes - i, posColonnes).typePoint == "#":
                murNord = True
                rayonNord = i

        if(not murEst):
            if matrice.getPoint(posLignes, posColonnes + i).typePoint == "-":
                pass
            if matrice.getPoint(posLignes, posColonnes + i).typePoint == ".":
                if not matrice.getPoint(posLignes, posColonnes + i).isCovered:
                    score+=1

        if(not murSud):
            if matrice.getPoint(posLignes + i, posColonnes).typePoint == "-":
                pass
            if matrice.getPoint(posLignes + i, posColonnes).typePoint == ".":
                if not matrice.getPoint(posLignes + i, posColonnes).isCovered:
                    score+=1

            if matrice.getPoint(posLignes + i, posColonnes).typePoint == "#":
                murSud = True
                rayonSud = i

        if(not murOuest):
            if matrice.getPoint(posLignes, posColonnes - i).typePoint == "-":
                pass
            if matrice.getPoint(posLignes, posColonnes - i).typePoint == ".":
                if not matrice.getPoint(posLignes, posColonnes - i).isCovered:
                    score+=1

            if matrice.getPoint(posLignes, posColonnes - i).typePoint == "#":
                murOuest = True
                rayonOuest = i

    rayonN = rayonNord
    rayonE = rayonEst
    rayonS = rayonSud
    rayonO = rayonOuest


    #Nord
    for i in range(posLignes, posLignes - 1 - rayonNord, -1):
        for j in range(posColonnes + 1, posColonnes + 1+  rayonE, +1):

            if not matrice.getPoint(i, j).typePoint == "-" and not matrice.getPoint(i, j).typePoint == "#":
                if not matrice.getPoint(i,j).isCovered:
                    score+=1

            elif matrice.getPoint(i, j).typePoint == "#":
                rayonE = j - posColonnes
                break

    #Est
    for j in range(posColonnes +1 , posColonnes + 1 + rayonEst, +1):
        for i in range(posLignes + 1, posLignes + 1 + rayonS, +1):

            if not matrice.getPoint(i, j).typePoint == "-" and not matrice.getPoint(i, j).typePoint == "#":
                if not matrice.getPoint(i,j).isCovered:
                    score+=1

            elif matrice.getPoint(i, j).typePoint == "#":
                rayonS = i - posLignes
                break

    #Sud
    for i in range(posLignes, posLignes + 1 + rayonSud, + 1):
        for j in range(posColonnes, posColonnes -1 - rayonO, -1):

            if not matrice.getPoint(i, j).typePoint == "-" and not matrice.getPoint(i, j).typePoint == "#":
                if not matrice.getPoint(i,j).isCovered:
                    score+=1

            elif matrice.getPoint(i, j).typePoint == "#":
                rayonO = posColonnes - j - 1
                break

    #Ouest
    for j in range(posColonnes, posColonnes - 1 - rayonOuest, -1):
        for i in range(posLignes - 1, posLignes - 1 - rayonN, -1):

            if not matrice.getPoint(i, j).typePoint == "-" and not matrice.getPoint(i, j).typePoint == "#":
                if not matrice.getPoint(i,j).isCovered:
                    score+=1

            elif matrice.getPoint(i, j).typePoint == "#":
                rayonN = posLignes - i - 1
                break

    score+=1
    return score

def positionnerRouteur(mat):
        routersOpti=[]
        #Parcours des cellules en trouvant les cas maximaux
        for i in mat.targetList2.keys(): #parcours les lignes des targets
            j=0
            while j< len(mat.targetList2[i]):
                murTrouve=False
                for k in range(i-mat.routerRange,i+mat.routerRange): #parcours les lignes des walls
                    if k in mat.wallList2.keys():
                        for l in range(mat.targetList2[i][j]-mat.routerRange,mat.targetList2[i][j] + mat.routerRange): #parcours les colonnes des walls
                            if l in mat.wallList2[k]:
                                murTrouve=True
                                break
                if not murTrouve:#ajout d'un nouveau routeur
                    mat.getPoint(i,mat.targetList2[i][j]).isRouter=True
                    routersOpti.append([i,mat.targetList2[i][j]])
                    covering2(mat, mat.routerRange,i, mat.targetList2[i][j])
                    j-=1
                j+=1
        #Tant qu'il y a des cellules a couvrir (iMax != -1) on recherche le router avec le meilleur score
        while mat.targetList2:
            if len(routersOpti)*mat.routerCost>mat.budget*0.80 :
                mat.routerList = routersOpti
                mat.backboneList = BB_search.main(mat)
                if len(mat.routerList)*mat.routerCost + len(mat.backboneList)*mat.backboneCost > mat.budget: #Etude du dépassement du budget
                    mat.routerList.pop()
                    routersOpti.pop( )
                    mat.backboneList = BB_search.main(mat)
                    #Début de la recherche du placement le plus optimisé avec une certaine distance délimité par la distance induit du budget

                    marge = mat.budget - (len(mat.routerList)+1)*mat.routerCost - len(mat.backboneList)*mat.backboneCost
                    if marge > 0:
                        iMax=-1
                        jMax=-1
                        nbTargetMax=0
                        for i in mat.targetList2.keys(): #parcours les lignes des targets
                            j=0

                            while j< len(mat.targetList2[i]):

                                tmp = coveringScore(mat, mat.routerRange,i, mat.targetList2[i][j])
                                if(nbTargetMax<tmp):
                                    for m in routersOpti:
                                        if math.sqrt((m[0] - mat.targetList2[i][j])**2+(m[1] - i)**2) < marge *0.75:
                                            iMax = i
                                            jMax = j
                                            nbTargetMax=tmp
                                            break

                                j+=1
                        if iMax==-1:
                            break
                        mat.getPoint(iMax,mat.targetList2[iMax][jMax]).isRouter=True
                        ecrireLog("3 {} - {}   :  {}\n".format(iMax,jMax,nbTargetMax))
                        routersOpti.append([iMax,mat.targetList2[iMax][jMax]])
                        covering2(mat, mat.routerRange,iMax, mat.targetList2[iMax][jMax])

                    mat.backboneList = BB_search.main(mat)
                    return mat

            iMax=-1
            jMax=-1
            nbTargetMax=0
            for i in mat.targetList2.keys(): #parcours les lignes des targets
                j=0

                while j< len(mat.targetList2[i]):
                    tmp = coveringScore(mat, mat.routerRange,i, mat.targetList2[i][j])
                    if(nbTargetMax<tmp):
                        iMax = i
                        jMax = j
                        nbTargetMax=tmp
                    j+=1
            if iMax==-1:
                break
            mat.getPoint(iMax,mat.targetList2[iMax][jMax]).isRouter=True
            ecrireLog("2 {} - {}   :  {}\n".format(iMax,jMax,nbTargetMax))
            routersOpti.append([iMax,mat.targetList2[iMax][jMax]])
            covering2(mat, mat.routerRange,iMax, mat.targetList2[iMax][jMax])

        print(len(routersOpti))
        mat.routerList = routersOpti
        mat.backboneList = BB_search.main(mat)
        print("estPassé")

        return mat

#Fonction permettant d'ecrire le fichier .OUT
def ecrireFichier(router = [], backbone = []):

    filename = "output" + time.strftime("_%d_%m_%y__%H_%M") + ".out"

    try:
        os.mkdir("output")
    except:
        pass

    os.chdir("output/")
    f = open(filename,'a')

    if (backbone != []):
        line =  str(len(backbone)) + "\n"
        f.writelines(line)

        for b in backbone:
            line = str(b[0]) + " " + str(b[1]) + "\n"
            f.writelines(line)

    if (router != []):
        line =  str(len(router)) + "\n"
        f.writelines(line)

        for b in router:
            line = str(b[0]) + " " + str(b[1]) + "\n"
            f.writelines(line)

    f.close()

#Fonction permettant d'écrire des logs durant l'execution, afin de s'en servir comme "debug"
def ecrireLog(logs):
    fichier = open("log.txt", "a")
    fichier.write(logs)
    fichier.close()


if __name__ == '__main__':
    try:
        os.remove("log.txt")
    except: pass
    mat=lectureFichier("maps/lets_go_higher.in")
    mat=positionnerRouteur(mat)
    for compteurLignes in range(mat.rows):
         for compteurColonnes in range(mat.columns):
                if(mat.getPoint(compteurLignes,compteurColonnes).typePoint == "."):
                    if(mat.getPoint(compteurLignes,compteurColonnes).isCovered):
                        if mat.getPoint(compteurLignes,compteurColonnes).isRouter:
                            print("R",end='')
                        else:
                            print(".",end='')
                    else:
                        print("X",end='')
                elif(mat.getPoint(compteurLignes,compteurColonnes).typePoint == "#"):
                    print("#",end='')
                else:
                    print("-",end='')
         print()
    ecrireFichier(mat.routerList,mat.backboneList)
