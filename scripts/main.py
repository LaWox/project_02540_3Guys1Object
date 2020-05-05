import cv2
import cameraRig 
import camera 
import numpy as np 

def someTestingStuff(rig):
    cPath1 = "data/pictures/Jussi/calibration_jussi_resized/"
    cPath2 = "data/pictures/Platon/calibration_platon_resized/"
    cPath3 = "data/pictures/William/calibration_william/"

    camera1 = camera.Camera(cPath1, "hejehj", cameraNr = 0, calibrated = True)
    camera2 = camera.Camera(cPath2, "hejehj", cameraNr = 1, calibrated = True)
    camera3 = camera.Camera(cPath3, "hejehj", cameraNr = 2, calibrated = True)
    print('calibrated cameras done!')

    cameras = [camera1, camera2, camera3]
    newRig = cameraRig.Rig(cameras, calibrated = True)
    print('calibrated rig done!')

if __name__ == "__main__":
   someTestingStuff()