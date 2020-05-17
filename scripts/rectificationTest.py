from camera import Camera
from imageProcessing import rectifyImage, loadPictures
import glob
import numpy as np


def createKFromTextFile(path):
    textList = [open(file).read() for file in sorted(glob.glob(path + "*.txt"))]

    kList = []
    for k in range(0,len(textList)):
        textRows = textList[k].split('\n')
        count = 0
        K = np.empty((3, 3))
        for i in range(1, 4):
            rowList = textRows[i].split(' ')
            for j in range(0, 3):
                K[count, j] = float(rowList[j])
            count += 1
        kList.append(K)


    return kList





calibrationPath1 = "data/Pictures/Jussi/calibration_jussi_resized/"
objPath1 = "data/Pictures/Jussi/cornflakes_jussi_resized/"
calibrationPath2 = "data/Pictures/Platon/calibration_platon_resized/"
objPath2 = "data/Pictures/platon/cornflakes_platon_resized/"

calibList=createKFromTextFile(Cpath)
images=loadPictures(ObjPath,".ppm")