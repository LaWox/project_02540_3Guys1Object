import cv2
import cameraRig 
import camera 
import numpy as np 
import featureDetMatch as fdm
import denseMapping as dm

def someTestingStuff():
    cPath1 = "data/pictures/Jussi/calibration_jussi_resized/"
    cPath2 = "data/pictures/Platon/calibration_platon_resized/"
    cPath3 = "data/pictures/William/calibration_william/"

    objPath1 = "data/pictures/Jussi/cornflakes_jussi_resized/"
    objPath2 = "data/pictures/Platon/cornflakes_platon_resized/"
    objPath3 = "data/pictures/William/cornflakes_william/"

    camera1 = camera.Camera(cPath1, objPath1, cameraNr = 0, calibrated = True)
    camera2 = camera.Camera(cPath2, objPath2, cameraNr = 1, calibrated = True)
    camera3 = camera.Camera(cPath3, objPath3, cameraNr = 2, calibrated = True)

    cameras = [camera1, camera2, camera3]
    newRig = cameraRig.Rig(cameras, calibrated = True, verbose=1)

    matches = fdm.getMatches(newRig, 30)
    densemapping = dm.propogateMatches(matches, 5, 11)
    densemapping = np.asarray(densemapping)
    print(densemapping.shape)

if __name__ == "__main__":
   someTestingStuff()