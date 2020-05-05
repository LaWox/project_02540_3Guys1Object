import numpy as np 
import cv2 
import glob
import matplotlib.pyplot as plt

# BOARD_DIMS = (22, 13)
# BOARD_DIMS = (8, 6)
BOARD_DIMS = (10, 7)

class Camera:
    ''' Holds camera atributes
    Parameters:
        string calibrationImgPath: path to calibration images
        int cameraNr: number of the camera, like an id
        npArr K: intridtic matrix of the camera TODO: probably remove this one
        boolean calibrated: if calibrated or not 
    '''
    def __init__(self, calibrationImgPath, objImgPath, cameraNr = 0, K = [], calibrated = False):
        self.K = []
        self.objImgPath = objImgPath                 # path to cameras picture of object 
        self.calibrationImgPath = calibrationImgPath # path to folder where calibration images are
        self.calibrationPoints = []
        self.objPoints = []
        self.cameraNr = cameraNr
        
        self.imgPaths = self.__setImgPaths()
        if calibrated:
            self.K = self.__getKFromFile() # get calibrated K from file
            self.calibrationPoints = self.__getCalibrationPointsFromFile()
            self.objPoints = self.__getObjPointsFromFile()

        else: # save new data if not already calculated
            self.__calibrate() 
            self.__saveK() 
            self.__saveCalibrationPoints()
            self.__saveObjPoints()
        return 

    def __calibrate(self):
        print(f'calibrating camera {self.cameraNr}')
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # calibrate camera with checkboard images 
        images = self.__getCalibrationImages()
        objPoints = []
        imgPoints = []
        gray = []

        objP = getObjPoints() # make checkersPoints 
        counter = 1 
        for img in images:
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, BOARD_DIMS, None)
            
            print(f"corners found {ret}")
            print(f"image nr:{counter} being processed")
            counter += 1
            if ret: # if it finds the corners
                accuCorners = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                objPoints.append(objP)
                imgPoints.append(accuCorners)
        
        objPoints = np.asarray(objPoints).astype(np.float32)
        imgPoints = np.asarray(imgPoints)

        self.objPoints = objPoints
        self.calibrationPoints = imgPoints
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objPoints, imgPoints, gray.shape[::-1],None,None)

        self.K = mtx
        return 

    def __saveK(self):
        np.save("data/cameraData/camera" + str(self.cameraNr) + '/kMatrix', self.K)
        return 

    def __saveCalibrationPoints(self):
        np.save("data/cameraData/camera" + str(self.cameraNr) + '/calibrationPoints', self.calibrationPoints)
    
    def __saveObjPoints(self):
        np.save("data/cameraData/camera" + str(self.cameraNr) + '/objPoints', self.objPoints)
    
    def __getKFromFile(self):
        K = np.load("data/cameraData/camera" + str(self.cameraNr) + '/kMatrix' + '.npy')
        return K  

    def __getCalibrationPointsFromFile(self):
        points = np.load("data/cameraData/camera" + str(self.cameraNr) + '/calibrationPoints' + '.npy')
        return points

    def __getObjPointsFromFile(self):
        points = np.load("data/cameraData/camera" + str(self.cameraNr) + '/objPoints' + '.npy')
        return points

    def __getCalibrationImages(self):
        images = [cv2.imread(file) for file in glob.glob(self.calibrationImgPath + "*.jpg")]
        return images 
    
    def __setImgPaths(self):
        images = [str(file) for file in glob.glob(self.objImgPath + "*.png")]
        return images

    def getCalibrationPoints(self):
        return self.calibrationPoints

    def getObjPoints(self):
        return self.objPoints

    def getImages(self):
        # get images associated with this camera from path parameter
        images = [cv2.imread(file) for file in glob.glob(self.objImgPath + "*.png")]
        return images

    def getImg(self, idx):
        ''' gets a specific image from the folder of images
        Parameters:
            idx: index of image to be retreived 
        Returns:
            img: the image object
        '''
        return cv2.imread(self.imgPaths[idx], cv2.IMREAD_GRAYSCALE)

    def getK(self):
        # return intristic matrix
        return self.K

    def getCameraNo(self):
        return self.cameraNr

def getObjPoints(squareLength = 30):
        ''' returns manifacturd objPoints for calibration
        Parameters:
            int squareLength: length of the square of the calibration obj
        Returns:
            npArr objPoints: arrar of 3d points
        '''
    objPoints = []
    for i in range(BOARD_DIMS[0]):
        for j in range(BOARD_DIMS[1]):
            point = (i*squareLength, j*squareLength, 0.0)
            objPoints.append(point)
    return np.asarray(objPoints)

if __name__ == "__main__":
    calibrationPath = "data/calibrationImgs/camera0/"
    objPath = "hejehje"
    camera = Camera(calibrationPath, objPath, calibrated=True)
