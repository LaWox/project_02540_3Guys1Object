# Triangulering

import cv2 
import numpy as np


def get3dPoints(pList, featuresList):
    #points3d=np.empty((int(np.floor(len(pList)/2)),len(featuresList),len(featuresList[0])))
    points3D=[]
    count=0
    for x in range(0,len(pList)-1):
        Q=cv2.triangulatePoints(pList[x],pList[x+1],featuresList[x],featuresList[x+1])
        Q/= Q[3] #diving by w

        #points3d[count]=Q[:]
        points3D.append(Q[:])
    return points3D

def getError(pList,featList, pointsL):
    count=0;
    maxIndx = int(np.floor(len(pList)/2))
    for x in range(0,maxIndx):
        P1 = pList[x]
        P2 = pList[x+1]
        f1=featList[x]
        f2=featList[x+1]
        points=pointsL[count]

        pixel1 = P1 @ points
        pixel1 /= pixel1[2]
        pixel2 = P2 @ points
        pixel2 /= pixel2[2]

        error1 = np.sqrt(np.sum((f1 - pixel1[:1]) ** 2))/len(f1[0])
        error2 = np.sqrt(np.sum((f2 - pixel2[:1]) ** 2))/len(f2[0])
        print('Error in cam1',error1,'Error in cam2',error2)

        count += 1



P1 = np.eye(4)[:3]
P2 = np.array([[ 0.878, -0.01 ,  0.479, -1.995],
            [ 0.01 ,  1.   ,  0.002, -0.226],
            [-0.479,  0.002,  0.878,  0.615],
            ])
# Homogeneous arrays
a3xN = np.array([[ 0.091,  0.167,  0.231,  0.083,  0.154],
              [ 0.364,  0.333,  0.308,  0.333,  0.308],
              ])
b3xN = np.array([[ 0.42 ,  0.537,  0.645,  0.431,  0.538],
              [ 0.389,  0.375,  0.362,  0.357,  0.345],
              ])

points=get3dPoints([P1,P2],[a3xN,b3xN])


getError([P1,P2],[a3xN,b3xN],points)




if __name__ == "__main__":
    pass