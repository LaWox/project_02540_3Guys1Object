import numpy as np
import cv2
import glob

def loadPictures(path):
    """ Params:
            * path; is a string with a path to one folder with images from one camera """

    images=[cv2.imread(file) for file in glob.glob(path + "*.jpg")]
    return images

def chooseMinSize(imgs):
    """ Params:
        * imgs; is a list with one sample image from each camera"""
    minY = 1000000
    refCam = ""
    count=0
    for img in imgs:
        Y = img.shape[0]


        if (Y < minY):
            minY = Y
            refCam = count
        count += 1
    return (minY, refCam)

def resizeImg(imgs, sizeY):
    """ Params:
                * imgs; is a list with pictures from one camera
                * size; the minimum size which the image will be scaled with"""

    reSized = []
    ratio=sizeY/imgs[0].shape[0]
    width = int(imgs[0].shape[1] * ratio)
    height = int(imgs[0].shape[0] * ratio)
    dim = (width, height)
    for img in imgs:
        reSized.append(cv2.resize(img, dim, interpolation = cv2.INTER_AREA))


    #print('The old size was: '+str(imgs[0].shape))
    #print('The new size is: '+str(reSized[0].shape))
    return reSized


def main():
    cam1 = loadPictures("/Users/jussikangas/Desktop/Computer_vision/Pictures/Jussi/")
    print("cam1 loaded")
    cam2 = loadPictures("/Users/jussikangas/Desktop/Computer_vision/Pictures/platon/")
    print("cam2 loaded")

    print(len(cam1), len(cam2))
    test = [cam1[0],cam2[0]]
    minY, refCam = chooseMinSize(test)
    print("Min size chosen")
    print('The reference is camera: '+str(refCam))

    cameraListOriginal =[cam1, cam2]
    cameraListResized = []

    for x in range(0,len(cameraListOriginal)):
        if x != refCam:
            cameraListResized.append(resizeImg(cameraListOriginal[x], minY))
        else:
            cameraListResized.append(cameraListOriginal[x])

    print("Original size ",str(cam1[0].shape))
    print("Resized image ",str(cameraListResized[0][0].shape))
    print("Reference ",str(cam2[0].shape))

if __name__== "__main__" :
    main()













