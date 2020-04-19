# Feature detection and matching

import cv2 
import numpy as np 
import cameraRig
import camera
import matplotlib.pyplot as plt

def getFeatures(rig):
    '''
    input:
        rig --> an array of images responding to the different cameras
    returns:
        features --> for every image an array of features
    '''
    orb = cv2.ORB_create()
    cameras = rig.getCameras()
    features = []

    for camera in cameras:
        feats = []
        imgs = camera.getImages()
        for img in imgs:
            kp = orb.detect(img, None)
            kp, des = orb.compute(img, kp)
            feats.append(des)
    return 

def getMatching():
    
if __name__ == "__main__":
    cPath1 = "data/calibrationImgs/camera0/"
    cPath2 = "data/calibrationImgs/camera1/"

    objPath1 =  "data/objImages/camera0/"

    camera1 = camera.Camera(cPath1, objPath1, cameraNr = 0, calibrated = True)
    camera2 = camera.Camera(cPath2, "hejehj", cameraNr = 1, calibrated = True)
    
    cameras = [camera1, camera2]
    newRig = cameraRig.Rig(cameras, calibrated = True)

    getFeatures(newRig)