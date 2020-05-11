import cv2 as cv
import numpy as np 
from matplotlib import pyplot as plt
from camera import Camera
from cameraRig import Rig
from mpl_toolkits.mplot3d import Axes3D

def getDisparityMap(imgL, imgR):
    stereo = cv.StereoSGBM_create(numDisparities=32, blockSize=9)
    disparity = stereo.compute(imgL, imgR)
    return disparity

def getPoints(imgL, imgR, Q):
    disparity = getDisparityMap(imgL, imgR)
    points3d = cv.reprojectImageTo3D(disparity = disparity, Q = Q, handleMissingValues=False)
    return points3d

def plotSideBySide(imgL, imgR):
    f = plt.figure()
    f.add_subplot(1, 2, 1)
    plt.imshow(imgL)
    f.add_subplot(1, 2, 2)
    plt.imshow(imgR, cmap="gray")
    plt.show(block=True)

def plot3d(points):
    fig = plt.figure()
    ax = plt.axes(projection="3d")

    z_line = np.linspace(0, 15, 1000)
    x_line = np.cos(z_line)
    y_line = np.sin(z_line)
    ax.plot3D(x_line, y_line, z_line, 'gray')

    z_points = points[:][:][2]
    x_points = points[:][:][1]
    y_points = points[:][:][2]
    ax.scatter3D(x_points, y_points, z_points, cmap='hsv', s=1)
    plt.show()

if __name__ == "__main__":
    cPath1 = "data/pictures/Jussi/calibration_jussi_resized/"
    cPath2 = "data/pictures/Platon/calibration_platon_resized/"
    cPath3 = "data/pictures/William/calibration_william/"

    objPath1 = "data/pictures/Jussi/cornflakes_jussi_resized/"
    objPath2 = "data/pictures/Platon/cornflakes_platon_resized/"
    objPath3 = "data/pictures/William/cornflakes_william/"

    cam1 = Camera(cPath1, objPath1, cameraNr = 0, calibrated = True)
    cam2 = Camera(cPath2, objPath2, cameraNr = 1, calibrated = True)
    cam3 = Camera(cPath3, objPath3, cameraNr = 2, calibrated = True)

    cameras = [cam1, cam2, cam3]

    img1 = cam1.getImg(0)
    img2 = cam1.getImg(1)

    newRig = Rig(cameras, calibrated = True, verbose=1)

    Q = newRig.getQ(0, 1)

    points = getPoints(img1, img2, Q)
    print(points.shape)
    plot3d(points)


