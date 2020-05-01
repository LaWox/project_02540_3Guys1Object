import numpy as np
import cv2

def loadPictures(path):
    """ Params:
            * path; is a string with a path to one folder with images from one camera """

        images=[cv2.imread(file) for file in glob.glob(path.calibrationImgPath + "*.png")]
        return images

def chooseMinSize(imgs):
    """ Params:
        * imgs; is a list with one sample image from each camera"""
    minY = 1000000
    for img in imgs:
        Y = img.shape[0]

        if (Y < minY):
            minY = Y
    return minY

def resizeImg(imgs, size):
    """ Params:
                * imgs; is a list with pictures from one camera
                * size; the minimum size which the image will be scaled with"""

    #https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/




