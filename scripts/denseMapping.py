import numpy as np 
import featureDetMatch as fdm
import camera
import cameraRig
from heapq import heappush, heappop
import time

def propogateMatches(matches, radius, patchSize):
    ''' find more matches from original matches 
    '''
    z = 0.9 # TODO: change these later
    t = 0.01
    S_DIRECTIONS = np.asarray([[1, 0], [-1, 0], [0, 1], [0, -1]])

    mapping = []
    seeds = []
    disp = np.floor(radius/2)

    addedPosDict1 = {} 
    addedPosDict2 = {}
    consideredPosDict = {}

    for arr in matches:
        for match in arr:
            p1, p2 = match.getPoints()
            
            patch1 = getPatch(p1.getImg(), p1.getCoords(), patchSize)
            patch2 = getPatch(p2.getImg(), p2.getCoords(), patchSize)

            val = zncc(patch1, patch2) # calc the zncc value between match 
            match.setZncc(val)
            heappush(seeds, match) # make a heap out of previous matches
            mapping.append(match) # add all previous matches to the mapping
    i = 0
    currCameraPair = ()
    currImgIdx = None

    while len(seeds) != 0:
        i+= 1
        print(f'propagating match {i}')

        match = heappop(seeds)
        p1, p2 = match.getPoints()

        newCameraPair = (p1.getCamera().getCameraNo, p2.getCamera().getCameraNo)
        newImgIdx = p1.getImgIdx()

        # reset the point dictionary whenever we change camera or picture 
        if(newCameraPair != currCameraPair or newImgIdx != currImgIdx):
            posDict1 = {}
            posDict2 = {}
            consideredPosDict = {}
            print('new Setup')

        p1Pos = p1.getCoords()
        p2Pos = p2.getCoords()
        
        if((tuple(p1Pos) + tuple(p2Pos)) in consideredPosDict):
            continue

        consideredPosDict[(tuple(p1Pos) + tuple(p2Pos))] = "true"

        for x in range(radius):
            for y in range(radius):
                # adjust pos for new points
                coords1 = getNewCoords(p1Pos, disp, (x, y)) 
                coords2 = getNewCoords(p2Pos, disp, (x, y))

                # enforce disparity gradient
                if np.max((coords1-p1Pos)-(coords2-p2Pos)) > 1:
                    continue

                # enforce uniqueness before calculations 
                if(tuple(coords1) not in posDict1 and tuple(coords2) not in posDict2):
 
                    s1 = calcS(coords1, p1.getImg(), S_DIRECTIONS)
                    if s1 > t:
                        s2 = calcS(coords2, p2.getImg(), S_DIRECTIONS)
                    if s2 > t:
                        # check s first so to not do uneccesary calculations
                        newPatch1 = getPatch(p1.getImg(), coords1, patchSize) 
                        newPatch2 = getPatch(p2.getImg(), coords2, patchSize)
                        val = zncc(newPatch1, newPatch2)
                        
                        if val > z:
                            # add points to dict
                            addedPosDict1[tuple(coords1)] = "True"
                            addedPosDict2[tuple(coords2)] = "True"

                             # generate new points
                            newPoint1 = p1.getNewPoint(coords1) 
                            newPoint2 = p2.getNewPoint(coords2)
                            
                            # gen new match  
                            newMatch = fdm.Match(newPoint1, newPoint2, zncc=val)

                            # add new match to the heap
                            heappush(seeds, newMatch) 
                            mapping.append(newMatch)  
                            print('found new Match')
                            


    print('after: ', len(mapping))
    return mapping

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

def calcS(pos, img, directions):
    ''' calculate the value S enshures more similiarity between points
    Parameters:
        tuple pos : holds the coord of the point
    Returns:
        float s: the value S 
    '''
    gradients = np.empty(4)
    y, x = pos.astype(int)

    # calc gradients in directions
    i = 0
    centerIntensity = int(img[x][y])
    for dirr in directions:
        dX = x + dirr[0]
        dY = y + dirr[1]

        gradients[i] =  centerIntensity- int(img[dX][dY])
        i += 1

    s = np.max(gradients) # return the biggest gradient
    return s

def zncc(window1, window2):
    win1 = window1.flatten()
    win2 = window2.flatten()

    # compute avgs
    avg1 = np.mean(win1)
    avg2 = np.mean(win2)
  
    # compute std
    std1 = np.std(win1)
    std2 = np.std(win2)

    corr = (np.abs(win1 - avg1)).dot((np.abs(win2 - avg2)))
    corr /= (std1*std2*win1.size)
    return corr 

def printSetup(match):
    p1, p2 = match.getPoints()
    c1 = p1.getCamera()
    c2 = p2.getCamera()

    print(c1.getCameraNo(), c2.getCameraNo())

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
    denseMatches = propogateMatches(matches, 5, 11)
    print('done!')
    pass