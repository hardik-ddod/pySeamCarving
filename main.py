from PIL import Image as i
import numpy as n

# EFFECTS: Returns a numpy.array with same dimensions as the image.  Each
#          element contains the energy of the corresponding pixel.
def findEnergyOfPixels(imgFilename):
    dxMatrix = findDxMatrix(imgFilename)
    dyMatrix = findDyMatrix(imgFilename)
    energyMatrix = n.add(dyMatrix, dxMatrix)
    return energyMatrix

# EFFECTS: Returns a numpy.array with the same dimensions of the image.  Each
#          element depresents the rate of change of the RBG values with respect
#          to elements before and after it.
def findDxMatrix(imgFilename):
    img = i.open(imgFilename)
    width, height = img.size
    rgbMatrix = n.asarray(img,int)
    col = []
    for y in range(height):
        row = []
        for x in range(width):
            if (x == 0):
                rx2 = rgbMatrix[y,1,0]
                rx1 = rgbMatrix[y,width-1, 0]
                dRx = rx2 - rx1
                gx2 = rgbMatrix[y,1,1]
                gx1 = rgbMatrix[y,width-1, 1]
                dGx = gx2 - gx1
                bx2 = rgbMatrix[y,1,2]
                bx1 = rgbMatrix[y,width-1, 2]
                dBx = bx2 - bx1
                dx = (dRx**2) + (dGx**2) + (dBx**2)
                row.append(dx)

            elif (x == (width - 1)):
                rx2 = rgbMatrix[y,0,0]
                rx1 = rgbMatrix[y,width-2, 0]
                dRx = rx2 - rx1
                gx2 = rgbMatrix[y,0,1]
                gx1 = rgbMatrix[y,width-2, 1]
                dGx = gx2 - gx1
                bx2 = rgbMatrix[y,0,2]
                bx1 = rgbMatrix[y,width-2, 2]
                dBx = bx2 - bx1
                dx = (dRx**2) + (dGx**2) + (dBx**2)
                row.append(dx)

            else:
                rx2 = rgbMatrix[y,x+1,0]
                rx1 = rgbMatrix[y,x-1, 0]
                dRx = rx2 - rx1
                gx2 = rgbMatrix[y,x+1,1]
                gx1 = rgbMatrix[y,x-1, 1]
                dGx = gx2 - gx1
                bx2 = rgbMatrix[y,x+1,2]
                bx1 = rgbMatrix[y,x-1, 2]
                dBx = bx2 - bx1
                dx = (dRx**2) + (dGx**2) + (dBx**2)
                row.append(dx)

        col.append(row)
    dxMatrix = n.array(col,int)
    return dxMatrix

# EFFECTS: Returns a numpy.array with the same dimensions of the image.  Each
#          element depresents the rate of change of the RBG values with respect
#          to elements above and below it.
def findDyMatrix(imgFilename):
    img = i.open(imgFilename)
    width, height = img.size
    rgbMatrix = n.asarray(img,int)
    col = []
    for y in range(height):
        row = []
        for x in range(width):
            if (y == 0):
                rx2 = rgbMatrix[1,x,0]
                rx1 = rgbMatrix[height-1,x, 0]
                dRx = rx2 - rx1
                gx2 = rgbMatrix[1,x,1]
                gx1 = rgbMatrix[height-1,x, 1]
                dGx = gx2 - gx1
                bx2 = rgbMatrix[1,x,2]
                bx1 = rgbMatrix[height-1,x, 2]
                dBx = bx2 - bx1
                dx = (dRx**2) + (dGx**2) + (dBx**2)
                row.append(dx)

            elif (y == (height - 1)):
                rx2 = rgbMatrix[0,x,0]
                rx1 = rgbMatrix[height-2,x, 0]
                dRx = rx2 - rx1
                gx2 = rgbMatrix[0,x,1]
                gx1 = rgbMatrix[height-2,x, 1]
                dGx = gx2 - gx1
                bx2 = rgbMatrix[0,x,2]
                bx1 = rgbMatrix[height-2,x, 2]
                dBx = bx2 - bx1
                dx = (dRx**2) + (dGx**2) + (dBx**2)
                row.append(dx)

            else:
                rx2 = rgbMatrix[y+1,x,0]
                rx1 = rgbMatrix[y-1,x, 0]
                dRx = rx2 - rx1
                gx2 = rgbMatrix[y+1,x,1]
                gx1 = rgbMatrix[y-1,x, 1]
                dGx = gx2 - gx1
                bx2 = rgbMatrix[y+1,x,2]
                bx1 = rgbMatrix[y-1,x, 2]
                dBx = bx2 - bx1
                dx = (dRx**2) + (dGx**2) + (dBx**2)
                row.append(dx)

        col.append(row)
    dyMatrix = n.array(col,int)
    return dyMatrix

# EFFECTS:  Takes an energy matrix of an image as an input.  Using dynamic
#           programming, returns numpy.array where each element represents
#           the minimum energy required to get to that pixel.
def findVerticalPathEnergies(energyMatrix):
    h, w = energyMatrix.shape
    dpPathMatrix = []
    dpPathMatrix.append(list(energyMatrix[0]))

    for y in range(1, h):
        row = []
        for x in range(w):
            curr = min(dpPathMatrix[y-1][(x-1 + w)%w],dpPathMatrix[y-1][x%w],dpPathMatrix[y-1][(x+1)%w])
            curr = curr + energyMatrix[y,x]
            row.append(curr)
        dpPathMatrix.append(row)
    dpPathMatrix = n.array(dpPathMatrix)
    return dpPathMatrix

# EFFECTS: Takes pathMatrix of an image as an input.  Returns the seam containing
#          the least energy.
def findVerticalSeam(pathMatrix):
    seamArray = []
    height, width = pathMatrix.shape
    smallestEnergyPathEndX = findIndexOfSmallestValueInList(list(pathMatrix[height-1]))
    seamArray.append(smallestEnergyPathEndX)
    for y in range(1, height):
        if (smallestEnergyPathEndX == 0):
            currIndex = 0
            currMin = pathMatrix[height-1-y, 0]
            if (currMin >= pathMatrix[height-1-y, 1]):
                currIndex = 1
            seamArray.append(currIndex)
            smallestEnergyPathEndX = currIndex
        elif (smallestEnergyPathEndX == (width - 1)):
            currIndex = width - 1
            currMin = pathMatrix[height - 1 - y, width - 1]
            if (currMin >= pathMatrix[height-1-y, width - 2]):
                currIndex = width-2
            seamArray.append(currIndex)
            smallestEnergyPathEndX = currIndex
        else:
            currIndex = smallestEnergyPathEndX - 1
            # print(currIndex)
            currMin = pathMatrix[(height-1-y),(smallestEnergyPathEndX-1)]
            if(currMin <= pathMatrix[height-1-y,smallestEnergyPathEndX] and currMin <= pathMatrix[height-1-y,smallestEnergyPathEndX+1]):
                seamArray.append(currIndex)
            else:
                currIndex = smallestEnergyPathEndX
                # print(currIndex)
                currMin = pathMatrix[height-1-y,smallestEnergyPathEndX]
                if(currMin <= pathMatrix[height-1-y,smallestEnergyPathEndX-1] and currMin <= pathMatrix[height-1-y,smallestEnergyPathEndX+1]):
                    seamArray.append(currIndex)
                else:
                    currIndex = smallestEnergyPathEndX + 1
                    # print(currIndex)
                    currMin = pathMatrix[height-1-y,smallestEnergyPathEndX+1]
                    if(currMin <= pathMatrix[height-1-y,smallestEnergyPathEndX-1] and currMin <= pathMatrix[height-1-y,smallestEnergyPathEndX]):
                        seamArray.append(currIndex)

            smallestEnergyPathEndX = currIndex
            # print(smallestEnergyPathEndX)
            # print(seamArray)
    seamArray.reverse()
    return seamArray

# EFFCTS: return index of smalles value in an array
def findIndexOfSmallestValueInList(inList):
    index = 0
    for i in range(len(inList)):
        if(inList[i] <= inList[index]):
            index = i
    return index

# EFFECTS:  Takes a list of pixels and removes them from the image corresponding
#           to the path variable imgFilename.  Then, stores resulting image at
#           destination path.
def removeSeam(imgFilename, seamList, destination):
    img = i.open(imgFilename)
    width, height = img.size
    imgPixelData = n.asarray(img, int)
    print(imgPixelData.shape)
    retPixelData = n.empty((height,width))
    for y in range(height):
        for x in range(width):
            if seamList[y] == x:
                retPixelData[y,x] = False
            else:
                retPixelData[y,x] = True
    print(retPixelData.shape)
    resizedPixelData = n.empty((height-1,width-1,3))
    col = []
    for y in range(height):
        for x in range(width):
            if retPixelData[y,x] == 1:
                col.append(tuple(imgPixelData[y,x]))
            # else:
            #     col.append(tuple([255, 0, 0]))

    img2 = i.new('RGB', (width-1,height))
    img2.putdata((col))
    img2.save(destination)

# EFFECTS: pipeline function to resize image once.  Takes image from imgFilename
#          and stores it at destination.
def resize(imgFilename, destination):
    energyMatrix = findEnergyOfPixels(imgFilename)
    pathMatrix = findVerticalPathEnergies(energyMatrix)
    seamList = findVerticalSeam(pathMatrix)
    removeSeam(imgFilename, seamList, destination)

# EFFECTS:  Removes iter number of seams with the least energy from the image
def multipleResize(imgFilename, destination, iter):
    resize(imgFilename,destination)
    for i in range(iter-1):
        resize(destination, destination)

# def makeImage(imgFilename, iter):




img = i.open("/Users/hardiksinghi/Desktop/new2.png")
em = n.array(([4,1,1,2,1,1,1],[3,1,2,3,2,1,0],[2,0,1,1,1,2,1],[1,0,1,2,3,2,1], [1,0,1,2,3,2,1]))
# print(em)
# print(findEnergyOfPixels("/Users/hardiksinghi/Desktop/new2.png"))
print(findVerticalSeam(findVerticalPathEnergies(findEnergyOfPixels("/Users/hardiksinghi/Desktop/new2.png"))))
# print(findVerticalPathEnergies(n.array(em)))
print(findVerticalSeam(findVerticalPathEnergies(em)))
multipleResize("/Users/hardiksinghi/Desktop/test.png", "/Users/hardiksinghi/Desktop/test2.png",150)
