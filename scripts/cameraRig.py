import numpy as np 
import camera

class Rig:
    def __init__(self, cameras = []):
        self.cameras = cameras
        self.homoGraphies = {}
        self.initHompgraphies()
        return 
    
    # create all homographies between cameras 
    def initHompgraphies(self):
        noCameras = len(self.cameras) # number of cameras in rig setup 
        for i in range(noCameras):
            for j in range(i+1, noCameras):
                # compute homogrpaphy here
                self.homoGraphies[str(i) + str(j)] = 1 # get homogrpahy here
    
    
    # get homography between cameras
    def getHomography(self, cam1, cam2):
        return self.homoGraphies[str(cam1) + str(cam2)]


if __name__ == "__main__":
    cPath1 = "../data/calibrationImgs/camera0/"
    cPath2 = "../data/calibrationImgs/camera1/"

    camera1 = camera.Camera(cPath1, "hejehj")
    camera2 = camera.Camera(cPath2, "hejehj")
    
    newRig = Rig([camera1, camera2])    
