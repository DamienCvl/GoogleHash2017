
def fichierSortie(router, backbone, cables):

    f = open('resultat.txt','w')

    retourChar = "\n"

    line = "backbone : [" + str(backbone[0]) + ";" + str(backbone[1]) + "]\n"
    f.writelines(line)

    f.writelines(retourChar)

    for i in range(len(router)):
        line = "routeur " + str(i+1) + " : [" + str(router[i][0]) + ";" + str(router[i][1]) + "]\n"
        f.writelines(line)

    f.writelines(retourChar)

    for i in range(len(cables)):
        line = "cable " + str(i+1) + " : [" + str(cables[i][0]) + ";" + str(cables[i][1]) + "]\n"
        f.writelines(line)

    f.close()


router = [[1,2],[3,4],[14,10]]
backbone = [1,1]
cables = [[2,3],[8,6],[4,4]]

fichierSortie(router, backbone, cables)