import numpy as np 
import featureDetMatch as fdm
import camera
import cameraRig
from heapq import heappush, heappop
import matplotlib.pyplot as plt

def propogateMatches(matches, radius, patchSize):
    z = 1 # TODO: change these later
    t = 1

    mapping = []
    seeds = []
    disp = np.floor(patchSize/2)
    addedPoints = {}

    for arr in matches:
        for match in arr:
            p1, p2 = match.getPoints()
            addedPoints = addMatchToDict(match, addedPoints)

            patch1 = getPatch(p1.getImg(), p1.getCoords(), patchSize)
            patch2 = getPatch(p2.getImg(), p2.getCoords(), patchSize)

            val = zncc(patch1, patch2) # calc the zncc value between match 
            match.setZncc(val)
            heappush(seeds, match) # make a heap out of previous matches
            mapping.append(match) # add all previous matches to the mapping

    i = 0
    while len(seeds) != 0:
        print(i+1)
        i += 1
        match = heappop(seeds)
        p1, p2 = match.getPoints()
    
        patch1 = getPatch(p1.getImg(), p1.getCoords(), patchSize)
        patch2 = getPatch(p2.getImg(), p2.getCoords(), patchSize)

        for x in range(patchSize):
            for y in range(patchSize):
                coords1 = p1.getCoords()
                coords1 = getNewCoords(coords1, disp, (x, y)) # adjust pos within the loop

                coords2 = p2.getCoords()
                coords2 = getNewCoords(coords2, disp, (x, y))

                newPatch1 = getPatch(p1.getImg(), coords1, patchSize) # get new patches from new coords
                newPatch2 = getPatch(p2.getImg(), coords2, patchSize)

                val = zncc(newPatch1, newPatch2)
                s1 = calcS(coords1, p1.getImg())
                s2 = calcS(coords2, p2.getImg())

                if val > z and s1 > t and s2 > t:
                    newPoint1 = p1.getNewPoint(coords1) #TODO: look into more
                    newPoint2 = p2.getNewPoint(coords2)
                    newMatch = fdm.Match(newPoint1, newPoint2, val)

                    print(val)
                    heappush(seeds, newMatch) # add new match to the heap

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
    ''' get a patch sourrounding the center 
    Arguments:
        img: img from which the patch is sourced
        center: center of patch 
        size: size of patch 
    Returns:
        patch: a patch of size*size
    '''
    x, y = center.astype(int)
    pad = int(np.floor(size/2))
    patch = img[y-pad:y+pad+1, x-pad:x+pad+1]
    return np.asarray(patch)

def calcS(pos, img):
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    gradients = np.empty(4)
    y, x = pos.astype(int)

    # calc gradients in 4 directions
    i = 0
    for dirr in directions:
        dX = x + dirr[0]
        dY = y + dirr[1]

        gradients[i] = int(img[x][y]) - int(img[dX][dY])
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
    cPath1 = "data/calibrationImgs/camera0/"
    cPath2 = "data/calibrationImgs/camera1/"
    objPath1 =  "data/objImages/camera0/"
    objPath2 =  "data/objImages/camera1/"

    camera1 = camera.Camera(cPath1, objPath1, cameraNr = 0, calibrated = True)
    camera2 = camera.Camera(cPath2, objPath2, cameraNr = 1, calibrated = True)
    
    cameras = [camera1, camera2]
    newRig = cameraRig.Rig(cameras, calibrated = True)

    matches = fdm.getMatches(newRig)
    propogateMatches(matches, 3, 5)
    print('done!')
    pass