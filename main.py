from Void import Void
from Wall import Wall
from Target import Target
from Matrice import Matrice

def lectureFichier(path):
    lineNumber = 0 # Numero de la ligne
    rowCount = 0 # Nombre de ligne
    matrice = Matrice()
    trouveTarget = False #permet de connaitre la premiere target rencontrée
    with open(path) as f: # On ouvre le fichier et on traite ligne par ligne
        for line in f:
            #On split les lignes dans les 3 premiers cas pour recuperer toutes les informations nécessaires tel
            #que le budget, le rayon,le cout,etc...
            if(lineNumber == 0):
                line1 = line.split()
            elif(lineNumber == 1):
                line2 = line.split()
            elif(lineNumber == 2):
                line3 = line.split()
            else:
                columnCount = 0
                for char in line: #Pour chaque char dans la ligne, on le traite en fonction de ce qu'il est
                    if char == '-': #Si c'est un tiret un crée un void
                        matrice.setPoint(rowCount,Void())
                    elif char == '#': #si c'est un hashtag on crée un wall
                        matrice.setPoint(rowCount,Wall()) #Sinon si c'est un point on crée un target
                    elif char == '.':
                        matrice.setPoint(rowCount,Target())
                        if(not trouveTarget): #tant qu'on ne la pas trouvée
                            premiereTarget = [rowCount, columnCount] #coordonnées de la premiere target
                    columnCount += 1 #On incrémente le nombre de colonne
                rowCount += 1 #On incrémente le nombre de ligne
                matrice.setLine()
            lineNumber += 1 #On incrémente le numéro de ligne

    rows = line1[0]
    columns = line1[1]
    routerRange = line1[2]

    backboneCost = line2[0]
    routerCost = line2[1]
    budget = line2[2]

    backboneInit = (line3[0],line3[1])

    return matrice, premiereTarget

 def covering(matrice, rayon, posX, posY):
     #parcours Ouest > Est afin de passer isCovered a True
     for i in range(posX - rayon, posX + rayon):
         for j in range(posY - rayon, posY + rayon):
             if not matrice(i, j) == 1 or not matrice(i, j) == 2:
                 matrice(i, j).isCovered = True
            else:
                j = posY + rayon

    #parcours Nord > Sud afin de passer isCovered a True
     for b in range(posY - rayon, posY + rayon):
         for a in range(posX - rayon, posX + rayon):
             if not matrice(a, b) == 1 or not matrice(a, b) == 2:
                 matrice(a, b).isCovered = True
             else:
                 a = posX + rayon

 def positionnerRouteur(matrice, premiereTarget):
     rowCount = premiereTarget[0]  #ligne du premier router
     columnCount = premiereTarget[1] #colomne du premier router
     compteurDeTarget = 0 #Permet de placer le router
     routers = [] #liste des positions des routeurs
     premiereExec =false #Premier passage pour partir du premier target

     for compteurLignes in range(240):
         for compteurColonnes in range(180):
             if not premiereExec: #premier passage
                 compteurLignes = rowCount
                 compteurColonnes = colomnCount
                 premiereExec = True

             if compteurDeTarget != 20 or not matrice[compteurLignes, compteurColonnes].getType() == 1 or not matrice[compteurLignes, compteurColonnes].getType() == 2:
                if not matrice[compteurLignes, compteurColonnes].isCovered :
                    compteurDeTarget = compteurDeTarget + 1
                    matrice[compteurLignes, compteurColonnes].isCovered = True
            else:
                if compteurDeTarget != 0:
                    routers.append(compteurLignes, compteurColonnes - compteurDeTarget/2)
                    compteurDeTarget = 0

print(lectureFichier("maps/charleston_road.in"))
