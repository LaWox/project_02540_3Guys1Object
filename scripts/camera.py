import numpy as np 
import cv2 
import calibration 
import glob


BOARD_DIMS = (22, 13)
# BOARD_DIMS = (8, 6)

# getting objPoints for calibration
def getObjPoints(squareLength = 30):
    objPoints = []
    for i in range(BOARD_DIMS[0]):
        for j in range(BOARD_DIMS[1]):
            point = (i*squareLength, j*squareLength, 0.0)
            objPoints.append(point)
    return np.asarray(objPoints)

class Camera:
    def __init__(self, calibrationImgPath, objImgPath, K = []):
        self.K = []                                  # Intristic matrix of camera
        self.objImages = objImgPath                  # path to cameras picture of object 
        self.calibrationImgPath = calibrationImgPath # path to folder where calibration images are
        pass

    def calibrate(self):
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # calibrate camera with checkboard images 
        images = [cv2.imread(file) for file in glob.glob(self.calibrationImgPath + "*.png")]
        objPoints = []
        imgPoints = []

        objP = getObjPoints() # make checkersPoints 
        
        counter = 1 
        for img in images:            
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, BOARD_DIMS, None)
            
            '''
            print(f"corners found {ret}")
            print(f"image nr:{counter} being processed")
            counter += 1
            '''
            if ret: # if it finds the corners
                accuCorners = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                objPoints.append(objP)
                imgPoints.append(accuCorners)
        
        objPoints = np.asarray(objPoints).astype(np.float32)
        imgPoints = np.asarray(imgPoints)
        
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objPoints, imgPoints, gray.shape[::-1],None,None)

        '''
        # checking error 
        tot_error =  0
        for i in range(len(objPoints)):
            imgpoints2, _ = cv2.projectPoints(objPoints[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv2.norm(imgPoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
            tot_error += error
        print ("mean error: ", tot_error/len(objPoints))
        '''
        
        self.K = mtx
        return 

    def getImages(self):
        # get images associated with this camera from path parameter
        pass

    def getK(self):
        # return intristic matrix
        return self.K

if __name__ == "__main__":
    calibrationPath = "../data/calibrationImgs/camera0/"
    objPath = "hejehje"
    camera = Camera(calibrationPath, objPath)
    camera.calibrate()
    print(camera.getK())