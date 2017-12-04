from backbone_path.Edge import Edge
from backbone_path.Tree import Tree
from backbone_path.Router import Router
from operator import attrgetter

def link2Points(p1,p2): #cherche le chemin le plus court entre 2 points, return une liste de coordonnées
    if p1[1]>p2[1]: #tri du y le plus petit, p1 a le plus petit y
        p1,p2 = p2,p1
    path = [] #coord chemin parcouru
    x = p1[0]
    y = p1[1]

    if p1[0]<p2[0]: #si on a un décalage en diagonale en descente, on se déplace en diagonal vers le bas
        while x<p2[0] and y<p2[1]:#on se déplace jusqu'à tomber sur la même ligne ou même colonne
            y += 1
            x += 1
            path.append((x,y))

        if p2[0]==x: #cas sur la même ligne, deplacement que sur la ligne
            for i in range(y+1,p2[1]):
                path.append((x,i))

        if p2[1]==y: #cas sur la même colonne, deplacement uniquement en x
            for i in range(x+1,p2[0]): #descente vers p2
                path.append((i,y))

    elif p1[0]>p2[0]: #si on a un décalage en diagonale en montée, on se déplace en diagonal vers le haut
        while x>p2[0] and y<p2[1]:#on se déplace jusqu'à tomber sur la même ligne ou même colonne
            y += 1
            x -= 1
            path.append((x,y))

        if p2[0]==x: #cas sur la même ligne, deplacement que sur la ligne
            for i in range(y+1,p2[1]):
                path.append((x,i))

        if p2[1]==y: #cas sur la même colonne, deplacement uniquement en x
            for i in range(x-1,p2[0],-1): #montée vers p2
                path.append((i,y))

    return path

def sortEdge(ListRouter):

    ListEdge = []
    ListR=ListRouter[:]
    for A in ListR:
        ListR = ListR[1:len(ListR)]
        for B in ListR:

            xA = A.pos[0]
            yA = A.pos[1]
            xB = B.pos[0]
            yB = B.pos[1]

            dist = max(abs(yB-yA),abs(xB-xA))

            ListEdge.append(Edge(A,B,dist))

    ListEdge.sort(key=attrgetter("distance"))
    return ListEdge

def edgePlacement(AllRouter): # sélectionne les arêtes à placer pour avoir un arbre couvrant minimal (Algo de Prim)
    #AllRouter doit être une liste d'objet Router de même que initBackbone est un objet Router
    ListEdgeSorted = sortEdge(AllRouter)
    trees = []
    edgeToLink = []
    numTree = 0
    for edge in ListEdgeSorted: # permet de placer les aretes et les routeurs dans des arbres sans faire de boucle
        numtree1 = edge.router1.inWhichTree
        numtree2 = edge.router2.inWhichTree
        if numtree1 != None and numtree2 != None: # si les routeurs de l'arete sont associé à des arbres
            if numtree1 == numtree2: # et qu'ils sont dans le même arbre, on passe à l'arete suivante
                continue
            elif len(trees[numtree1].routerIn) < len(trees[numtree2].routerIn): # (optimisation, on choisit l'arbre 1 comme celui qui a le moins de routeur)
                trees[numtree2].routerIn += trees[numtree1].routerIn # sinon on ajoute la liste des routeurs de l'arbres 1 à l'arbre 2
                for r in trees[numtree1].routerIn: # et on reassocie chaque routeur de l'arbre 1 à son nouvel arbre 2
                    r.inWhichTree = numtree2
            else:
                trees[numtree1].routerIn += trees[numtree2].routerIn
                for r in trees[numtree2].routerIn:
                    r.inWhichTree  = numtree1
        elif numtree1 != None: # un routeur n'a pas d'arbre, on l'associe à l'arbre de l'autre routeur
            edge.router2.inWhichTree = numtree1
            trees[numtree1].routerIn.append(edge.router2)
        elif numtree2 != None:
            edge.router1.inWhichTree = numtree2
            trees[numtree2].routerIn.append(edge.router1)
        else: # si aucun des routeurs n'a d'arbre, on crée un arbre et on lui ajoute les 2 routeurs
            edge.router1.inWhichTree = numTree
            edge.router2.inWhichTree = numTree
            trees.append(Tree())
            trees[numTree].routerIn.append(edge.router1)
            trees[numTree].routerIn.append(edge.router2)
            numTree += 1

        edgeToLink.append(edge) # on ajoute l'arête dans la liste d'arêtes à connecter

        if len(edgeToLink) == len(AllRouter)-1: #condition d'arret pour ne pas faire toute les aretes. On s'arrête dès qu'on a n-1 arêtes, car on aura n sommet connectés
            break

    return edgeToLink

                                                                                                                                  # |
'''def clearRightAngle(paths,mat):  # à pour but d'optimiser le nombre de backbones en enlevant les angles droits (ex de liaison possible   B - b - B où b est inutiles (à cause des diagonales), l'enlever réduit le budjet

    for l in paths:
        x=l[0]
        y=l[1]
        print("opti en cours")
        if (mat.getPoint(x+1,y).onBB == True or mat.getPoint(x-1,y).onBB == True) and (mat.getPoint(x,y+1).onBB == True or mat.getPoint(x,y-1).onBB == True):
            mat.getPoint(x,y).onBB == False
            print("bb {} {} supprimer".format(x,y))
            paths.remove(l)  # supprime le backbone de la liste
    print("opti fini")
    return 1'''

def main(mat):
    AllPoint = []
    AllCoord = mat.routerList[:]
    AllCoord.append(mat.backboneInit)
    for c in AllCoord:
        AllPoint.append(Router(c[0],c[1]))
    paths = []
    edges = edgePlacement(AllPoint)

    for edge in edges:
        paths += link2Points(edge.router1.pos,edge.router2.pos)
    
    for b in paths:
        x=b[0]
        y=b[1]
        mat.matrice[x][y].onBB = True
        
    backbones = mat.routerList + paths
    return backbones