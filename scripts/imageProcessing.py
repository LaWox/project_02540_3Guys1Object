import numpy as np
import cv2
import glob


def loadPictures(path, fileformat):
    """ fuction for loading pictures
    Params:
        * path; is a string with a path to one folder with images from one camera
        * fileformat: a file format ending like '.jpg' or '.png'
     Outputs:
        * images: a list with all of the images from the path folder
    """
    images=[cv2.imread(file) for file in sorted(glob.glob(path + "*"+fileformat))]
    return images

def chooseMinSize(imgs):
    """ find the min size of all images 
    Params:
        * imgs: is a list with one sample image from each camera
    Outputs:
        *minY: The smallest Y dimension for the cameras
        *refCam: The camera with the smallest Y dimension
    """
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
    """ resizing images
    Params:
        * imgs; is a list with pictures from one camera
        * size; the minimum size which the image will be scaled with
    Outputs:
        *reSized: a list with the resized images        
     """
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

def outputImgs(paths,imgs):
    """ writes images to new path
    Params:
        * paths; is a list with paths to the output folders
        * imgs; is a list with a list of images for each camera
    Outputs:
        * Returns nothing, but writes images to the path folder
    """
    count=0
    for path in paths:
        for x in range(0,len(imgs[count])): #change to 'range(0,len(imgs[count]))' if doing it for all the pictures
            name=str(x)+".jpg"
            filepath = path + name
            cv2.imwrite(filepath,imgs[count][x])
        count += 1
    print("The pictures were successfully outputted")


def rectifyImage(rig):
    """ rectifies all images in a camera
        Params:
            * rig; rig object, the camera rig containing the rectification transform
            * camera; a camera object, this is the reference camera
            * otherCameraNumber; int, the number of the other camera
        Outputs:
            * Returns imgsRect, a list containing the rectifies images
        """
    cameras=rig.getCameras()

    for i in range(0,len(cameras)):
        for j in range(i+1,len(cameras)) :
            imgs=cameras[i].getImages()
            R = rig.getRectifyTransform(cameras[i].getCameraNo(), j)
            P = rig.getProjectionTransformRectified(cameras[i].getCameraNo(), j)
            Ymap, Xmap=cv2.initUndistortRectifyMap(cameras[i].getK(),R=R,newCameraMatrix=P,map1=imgs[0].shape,map2=cv2.CV_32FC1)
            imgsRect=[]
            for x in range(0,len(imgs)):
                imgsRect.append(cv2.remap(imgs[x], Xmap, Ymap, cv2.INTER_LINEAR))
            cameras[i].updateImgs(imgsRect)
    rig.updateCameras(cameras)
    #https://stackoverflow.com/questions/53192333/problem-with-stereo-rectification-using-opencv-and-python

    return rig






def main():
    """
    When using these functions together, do first a trial run with only one picture from each camera to see which cameras has the smallest dimensions.
    After that you can manually change witch camera pictures you are supposed to change. The only thing you really need to worry about is the output
    path if images are written out. The output path needs to be in the same order as the cameras in the cameraListResized.

    """
    cam1 = loadPictures("/Users/jussikangas/Desktop/Computer_vision/Pictures/Jussi/human_jussi/",".jpg")
    print("cam1 loaded")
    cam2 = loadPictures("/Users/jussikangas/Desktop/Computer_vision/Pictures/Platon/human_platon/",".jpg")
    print("cam2 loaded")
    cam3 = loadPictures("/Users/jussikangas/Desktop/Computer_vision/Pictures/William/human_william/",".jpg")
    print("cam3 loaded")





    print(len(cam1), len(cam2), len(cam3))
    minY, refCam = chooseMinSize([cam1[0],cam2[0],cam3[0] ])
    print("Min size chosen")
    print('The reference is camera: '+str(refCam))

    cameraListOriginal =[cam1, cam2, cam3]
    cameraListResized = []


    for x in range(0,len(cameraListOriginal)):
        if x != refCam:
            cameraListResized.append(resizeImg(cameraListOriginal[x], minY))
        else:
            #cameraListResized.append(cameraListOriginal[x]) #Comment if writing any images, i.e. using outputImgs()
            continue

    print("Original size ",str(cam1[0].shape),str(cam2[0].shape))
    print("Resized image ",str(cameraListResized[0][0].shape),str(cameraListResized[1][0].shape))
    print("Reference ",str(cam3[0].shape))

    outputPath1 = "/Users/jussikangas/Desktop/Computer_vision/Pictures/Jussi/human_jussi/resized/"
    outputPath2 = "/Users/jussikangas/Desktop/Computer_vision/Pictures/platon/human_platon/resized/"
    outputImgs([outputPath1, outputPath2],cameraListResized)

if __name__== "__main__" :
    main()