# Feature detection and matching

import cv2 
import numpy as np 
import cameraRig
import camera
import matplotlib.pyplot as plt
import denseMapping

class Point:
    def __init__(self, coords, descriptor, color):
        self.coords2d = coords
        self.descriptor = descriptor
        self.imgPath = "pathToImg"
        self.color = color

    def setImg(self, path):
        self.imgPath = path
    
    def getImg(self):
        return cv2.imread(self.imgPath)

    def getCoords(self):
        return self.coords2d

    def getDescriptor(self):
        return self.descriptor

class Match:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
    
    def getPoints(self):
        return self.point1, self.point2


def getFeatures(rig):
    '''
    input:
        rig --> array of images responding to the different cameras
    returns:
        features --> for every image an array of features
    '''
    orb = cv2.ORB_create()
    cameras = rig.getCameras()
    features = []

    # extract features for all images in a camera
    for camera in cameras:
        feats = []
        imgs = camera.getImages()
        for img in imgs:
            kp = orb.detect(img, None)
            kp, des = orb.compute(img, kp)
            print(kp[0].pt)
            feats.append(des)
        features.append(feats) # features contains (noCamers * noImages * noFeatures) elements
    return features

def getMatches(rig):
    matches = []
    features = getFeatures(rig) # getFeatures returns all features for entire camera rig
    bf = cv2.BFMatcher_create(cv2.NORM_HAMMING, crossCheck=True) # brute force matching with hamming distance
    
    for i in range(len(features)):
        for j in range(i+1, len(features)):
                localMatches = []
                for imgIdx in range(len(features[i])):
                    desc1 = features[i][imgIdx]
                    desc2 = features[j][imgIdx]
                    match = bf.match(desc1, desc2)
                    localMatches.append(match)
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