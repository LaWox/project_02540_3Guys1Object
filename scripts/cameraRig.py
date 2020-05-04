import numpy as np 
import camera
import cv2 
import matplotlib.pyplot as plt

IMG_SHAPE = (1850, 1137)

class Rig:
    def __init__(self, cameras, calibrated = False):
        self.cameras = cameras
        self.homoGraphies = {}
        self.objP = cameras[0].getObjPoints() # uses square len of 30
        self.Rt = None #TODO: implement Rt

        # init homographies between the cameras
        if not calibrated:
            self.initHompgraphies()
        else:
            self.readHomographyFromFile()
        return 
    
    # create all homographies between cameras 
    def initHompgraphies(self):
        noCameras = len(self.cameras) # number of cameras in rig setup 
        # homographies = np.empty((np.math.factorial(noCameras-1), 3, 3))
        for i in range(noCameras):
            for j in range(i+1, noCameras):
                camera1 = self.cameras[i]
                camera2 = self.cameras[j]

                retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, t, E, F = cv2.stereoCalibrate(
                    camera1.getObjPoints(),
                    camera1.getCalibrationPoints(), # get calibration points
                    camera2.getCalibrationPoints(), 
                    IMG_SHAPE,
                    camera1.getK(), # get the camera matrixes
                    camera2.getK(),
                    None,
                    None
                    )
                self.homoGraphies[str(i) + str(j)] = (np.concatenate((R, t), axis = 1))
                np.save(("data/homographies/" + str(i) + str(j)), F)   # save F  

    def getCameras(self):
        return self.cameras
    # get already initialized homographies from file
    def readHomographyFromFile(self):
        noCameras = len(self.cameras) # number of cameras in rig setup 
        for i in range(noCameras):
            for j in range(i+1, noCameras):
                nr = str(i) + str(j)
                self.homoGraphies[nr] = np.load("data/homographies/" + nr + '.npy') 

    # get homography between cameras
    def getHomography(self, cam1, cam2):
        return self.homoGraphies[str(cam1) + str(cam2)]

    def getRt(self):
        return self.Rt
if __name__ == "__main__":
    cPath1 = "data/calibrationImgs/camera0/"
    cPath2 = "data/calibrationImgs/camera1/"

    camera1 = camera.Camera(cPath1, "hejehj", cameraNr = 0, calibrated = True)
    camera2 = camera.Camera(cPath2, "hejehj", cameraNr = 1, calibrated = True)
    
    cameras = [camera1, camera2]
    newRig = Rig(cameras, calibrated = True)
    rt = newRig.getHomography(0, 1)

    plt.imshow("data\calibrationImgs\camera0\frame0_0.png")
    plt.show()

