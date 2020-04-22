import cv2
import cameraRig 
import camera 
import numpy as np 

if __name__ == "__main__":
    cPath1 = "data/calibrationImgs/camera0/"
    cPath2 = "data/calibrationImgs/camera1/"

    camera1 = camera.Camera(cPath1, "hejehj", cameraNr = 0, calibrated = True)
    camera2 = camera.Camera(cPath2, "hejehj", cameraNr = 1, calibrated = True)
    
    cameras = [camera1, camera2]
    newRig = cameraRig.Rig(cameras, calibrated = True)