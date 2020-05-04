import numpy as np 
import camera
import cv2 
import matplotlib.pyplot as plt

IMG_SHAPE = (1850, 1137)

class Rig:
    ''' Rig containing several cameras
    Parameters:
        Camera[] cameras: array of Camera objects
        Bool calibrated: if it has been calibrated already or not
    '''
    def __init__(self, cameras, calibrated = False):
        self.cameras = cameras
        self.homoGraphies = {}
        self.objP = cameras[0].getObjPoints() # uses square len of 30
        self.Rt = None #TODO: implement Rt
        self.rectifyTranformations = {} #TODO: fix this

        # init homographies between the cameras
        if not calibrated:
            self.__initRig()
        else:
            self.__initFromFile()
        return 
    
    # create all homographies between cameras 
    def __initRig(self):
        ''' Initialise the rig by calibration
        Parameters:
            Self:
        Returns:
            None:
        '''
        noCameras = len(self.cameras) # number of cameras in rig setup 
        rectifyTransform = np.empty((2, 3, 3))

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

                # set and save the homography
                self.homoGraphies[str(i) + str(j)] = (np.concatenate((R, t), axis = 1))
                np.save(("data/homographies/" + str(i) + str(j)), F) #TODO this doesn't make any sense right now   

                # set and save rectifyTransorm
                returns = cv2.stereoRectify(
                    camera1.getK(), 
                    distCoeffs1, 
                    camera2.getK(),
                    distCoeffs2, 
                    IMG_SHAPE, 
                    R,
                    t,
                    rectifyTransform[0], # set rectifyTransorms in here
                    rectifyTransform[1]
                )
                self.rectifyTranformations[str(i) + str(j)] = (rectifyTransform)
                np.save(("data/rectifyTransforms/" + str(i) + str(j)), rectifyTransform)    

    def getCameras(self):
        return self.cameras

    def __initFromFile(self):
        ''' init Rig from already calculated metrics
        Parameters:
            Self:
        Returns:
            None:
        '''
        noCameras = len(self.cameras) # number of cameras in rig setup 
        for i in range(noCameras):
            for j in range(i+1, noCameras):
                nr = str(i) + str(j)
                self.homoGraphies[nr] = np.load("data/homographies/" + nr + '.npy')
                self.rectifyTranformations[nr] = np.load("data/rectifyTransforms/" + nr + '.npy') 
    
    def getHomography(self, cam1, cam2):
        ''' Returns homography between camera1 and camera 1
        Parameters:
            Camera cam1: camera 1
            Camera cam2: camera 2
        Returns:
            npArray homography: the homography between the two cameras
        '''
        return self.homoGraphies[str(cam1) + str(cam2)]

    def getRt(self):
        return self.Rt
    
    def getRectifyTransform(self, cameraNo1, cameraNo2):
        nr = str(cameraNo1) + str(cameraNo2)
        return self.rectifyTranformations[nr]

if __name__ == "__main__":
    cPath1 = "data/calibrationImgs/camera0/"
    cPath2 = "data/calibrationImgs/camera1/"

    camera1 = camera.Camera(cPath1, "hejehj", cameraNr = 0, calibrated = True)
    camera2 = camera.Camera(cPath2, "hejehj", cameraNr = 1, calibrated = True)
    
    cameras = [camera1, camera2]
    newRig = Rig(cameras, calibrated = True)
    rt = newRig.getHomography(0, 1)
    rec = newRig.getRectifyTransform(0, 1)
    print(rec[0])