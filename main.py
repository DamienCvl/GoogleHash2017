def lectureFichier(path):
    lineNumber = 0
    rowCount = 0
    tableauPoint = []
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
                    tableauPoint.append((rowCount,columnCount,char))
                    columnCount += 1
                rowCount += 1
            lineNumber += 1

    rows = line1[0]
    columns = line1[1]
    routerRange = line1[2]

    backboneCost = line2[0]
    routerCost = line2[1]
    budget = line2[2]

    backboneInit = (line3[0],line3[1])
    print(tableauPoint)

lectureFichier("maps/charleston_road.in")