# Feature detection and matching

import cv2 
import numpy as np 
import cameraRig
import camera
import matplotlib.pyplot as plt
import denseMapping

class Point:
    ''' store every keypoint in Point class
    Arguments:
        coords: coord of the point in 2d space
        color: color of the pixel 
        imgPath: path to the image
        descriptor: ORB descriptor of the keypoint 
    '''
    def __init__(self, coords, color, imgIdx, camera, descriptor = None):
        self.coords2d = coords
        self.descriptor = descriptor # TODO: Maybe this isn't needed
        self.imgIdx = imgIdx # TODO: how should this work?
        self.color = color
        self.camera = camera
    
    def __hash__(self): # for storing in dict
        return hash((self.camera.getCameraNo, self.imgIdx, self.coords2d[0], self.coords2d[1]))
    
    def __eq__(self, other): # for storing in dict
        return ((self.camera.getCameraNo, self.imgIdx, self.coords2d[0], self.coords2d[1]) == (other.camera.getCameraNo, other.imgIdx, other.coords2d[0], other.coords2d[1]))

    def getNewPoint(self, newCoords):
        ''' create new point whicch originates from self
        Parameters:
            newCoords: the coords of the new point
        Returns:   
            newPoint: the new Point() obj
        '''
        newPoint = Point(newCoords, self.color, self.imgIdx, self.camera, None) #TODO: color is wrong 
        return newPoint

    def setImg(self, path):
        self.imgPath = path
    
    def getImg(self):
        #return cv2.imread(self.imgPath)
        return self.camera.getImg(self.imgIdx)
    
    def getImgIdx(self):
        return self.imgIdx

    def getCamera(self):
        return self.camera

    def getCoords(self):
        return np.asarray(self.coords2d).astype(int)

    def getDescriptor(self):
        return self.descriptor


class Match:
    ''' Match consisting of two points
    Arguments:
        point1: first point
        point2: second point
    '''
    def __init__(self, point1, point2, zncc = 0.0):
        self.point1 = point1
        self.point2 = point2
        self.zncc = zncc

    def __lt__(self, other):
        return self.zncc < other.zncc

    def __hash__(self):
        return hash((self.point1, self.point2))
    
    def __eq__(self, other):
        return ((self.point1, self.point2) == (other.point1, other.point2))

    def getPoints(self):
        return self.point1, self.point2

    def getColor(self):
        meanColor=np.mean(np.array([self.point1.color, self.point2.color]), axis=0)
        return meanColor
 
    def getRt(self, rig):
        cameraNo1 = self.point1.camera.getCameraNo()
        cameraNo2 = self.point2.camera.getCameraNo()
        Rt = rig.getRt(cameraNo1, cameraNo2)
        return Rt
    
    def getImgIdx(self):
        idx = self.point1.imgIdx
        return idx

    def setZncc(self, value):
        self.zncc = value
    
def getFeatures(rig):
    ''' retreves the features from the rig
    Parameters:
        rig: array of images responding to the different cameras
    Returns:
        features: for every image an array of features
    '''
    if rig.verbose == 1:
        shouldPrint = True
    else:
        shouldPrint = False
    
    orb = cv2.ORB_create()
    cameras = rig.getCameras()
    features = []

    # extract features for all images in a camera
    for camera in cameras:
        feats = []
        imgs = camera.getRectifiedImages()# get rectified images with camera.getRectifiedImages and get normal with getImages()
        print(len(imgs))
        if(shouldPrint):
            print(f'Finding features in camera {camera.getCameraNo()}')
        for img in imgs:
            kp = orb.detect(img, None)
            kp, des = orb.compute(img, kp)
            feats.append((kp, des))
        features.append(feats) # features contains (noCamers * noImages * noFeatures) elements
    return features

def getMatches(rig, threshold = 50):
    ''' returns matches from the every camera pair
    Arguments:
        rig: a Rig object which holds the cameras and their pictures 
    Returns:
        matches: an array of Matches 
    '''
    if rig.verbose == 1:
        shouldPrint = True
    else:
        shouldPrint = False
    
    matches = []
    features = getFeatures(rig) # getFeatures returns all features for entire camera rig
    bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=True) # brute force matching with hamming distance
    cameras = rig.getCameras()
    
    for i in range(len(features)):
        for j in range(i+1, len(features)):
                if(shouldPrint):
                    print(f'Matching {i} <--> {j} : ', end='')
                
                localMatches = []
                for imgIdx in range(len(features[i])):
                   
                    if imgIdx > 3: #TODO: just for testing
                        break
                   
                    kp1 = features[i][imgIdx][0]
                    kp2 = features[j][imgIdx][0]

                    desc1 = features[i][imgIdx][1] # extract the descriptor
                    desc2 = features[j][imgIdx][1]

                    match = bf.match(desc1, desc2) # match the descriptors

                    for m in match: # loop through the matches to creta Points objects
                        if(m.distance < threshold): # threshholds the matches
                            queryIdx = m.queryIdx
                            trainIdx = m.trainIdx
                            pos1 = kp1[queryIdx].pt
                            pos2 = kp2[trainIdx].pt

                            p1 = Point(pos1, 0, imgIdx, cameras[i], None)
                            p2 = Point(pos2, 0, imgIdx, cameras[j], None) #TODO: stuff not added yet

                            mObj = Match(p1, p2)
                            localMatches.append(mObj)
                if(shouldPrint):
                    print(f'{len(localMatches)} matches found')
                matches.append(localMatches)
    return matches

if __name__ == "__main__":
    cPath1 = "data/calibrationImgs/camera0/"
    cPath2 = "data/calibrationImgs/camera1/"

    objPath1 =  "data/objImages/camera0/"
    objPath2 =  "data/objImages/camera1/"


    camera1 = camera.Camera(cPath1, objPath1, cameraNr = 0, calibrated = True)
    camera2 = camera.Camera(cPath2, objPath2, cameraNr = 1, calibrated = True)



    
    cameras = [camera1, camera2]
    newRig = cameraRig.Rig(cameras, calibrated = True)

    getMatches(newRig)