import numpy as np 
from featureDetMatch import Point, Match
from heapq import heappush, heappop

def propogateMatches(matches, radius, patchSize):
    z = 1 # TODO: change these later
    t = 1

    mapping = []
    seeds = []
    disp = np.floor(patchSize/2)
    addedPoints = {}

    for match in matches:
        p1, p2 = match.getPoints()
        addePoints = addMatchToDict(match, addedPoints)
        
        patch1 = getPatch(p1.getImg(), p1.coord2d, patchSize)
        patch2 = getPatch(p2.getImg(), p2.coord2d, patchSize)

        val = zncc(patch1, patch2) # calc the zncc value between match 
        heappush(seeds, (val, match)) # make a heap out of previous matches
        mapping.append(match) # add all previous matches to the mapping

    coords = [] # for saving coords of new point
    while len(seeds) != 0:
        match = heappop(seeds)
        p1, p2 = match.getPoints()
    
        patch1 = getPatch(p1.getImg(), p1.getCoords(), patchSize)
        patch2 = getPatch(p2.getImg(), p2.getCoords(), patchSize)

        for x in range(patchSize):
            for y in range(patchSize):
                coords1 = p1.getCoords() #TODO: getCoords needs to return np array
                coords1 = getNewCoords(coords1, disp, (x, y)) # adjust pos within the loop

                coords2 = p2.getCoords()
                coords2 = getNewCoords(coords2, disp, (x, y))

                newPatch1 = getPatch(p1.getImg(), coords1, patchSize) # get new patches from new coords
                newPatch2 = getPatch(p2.getImg(), coords2, patchSize)

                val = zncc(newPatch1, newPatch2)
                s1 = calcS(coords1, p1.getImg())
                s2 = calcS(coords2, p2.getImg())

                if zncc > z and s1 > t and s2 > t:
                    newPoint1 = Point() #TODO: fix this thing
                    newPoint2 = Point()
                    newMatch = Match(newPoint1, newPoint2)
                    heappush(seeds, (zncc, newMatch)) # add new match to the heap

                    # TODO: implement and enforce uniqueness before adding 
                    mapping.append(newMatch)

    return mapping

def addMatchToDict(match, pointDict):
    p1, p2 = match.getPoints()
    pointDict[p1] = "true"
    pointDict[p2] = "true"
    return pointDict

def getNewCoords(orgCoord, disp, xy):
    ''' helper function to shift coords in correct pos
    Paramters:
        orgCoords (np array): coords to be shifted
        disp (int): shift in coords, depends on patchSize
        xy (tuple): where in the patch we are currently
    
    Returns:
        coords (np array): new shifted coords
    '''
    x, y = xy
    coords = orgCoord - disp
    coords[0] += x
    coords[1] += y
    return np.asarray(coords)

def getPatch(img, center, size):
    x, y = center
    pad = int(np.floor(size/2))
    patch = img[y-pad:y+pad+1, x-pad:x+pad+1]
    return np.asarray(patch)

def calcS(pos, img):
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    gradients = np.empty(4)
    x, y = pos

    # calc gradients in 4 directions
    i = 0
    for dirr in directions:
        dX, dY = pos + dirr
        gradients[i] = img[x][y] - img[dX][dY]
        i += 1
    return np.max(gradients) # return the biggest gradient

def zncc(window1, window2):
    win1 = window1.flatten()
    win2 = window2.flatten()

    # compute avgs
    avg1 = np.mean(win1)
    avg2 = np.mean(win2)
    
    # compute std
    std1 = np.std(win1)
    std2 = np.std(win2)

    corr = 0
    for i in range(win1.shape[0]):
        corr += (win1[i] - avg1)*(win2[i] - avg2)
    
    corr /= (std1*std2)
    return corr 

if __name__ == "__main__":
    arr = [[1,2,3], [4,5,6], [7,8,9]]

    patch = getPatch(np.asarray(arr), (1,1), 3)
    print(patch)
    pass