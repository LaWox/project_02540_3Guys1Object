# Triangulering

import cv2 
import numpy as np


def get3dPoints(pList, featuresList):
    points3d=np.empty((len(pList),len(featuresList[0])))
    count=0
    for x in range(0,len(pList)-1):
        Q=cv2.triangulatePoints(pList[x],pList[x+1],featuresList[x],featuresList[x+1])
        Q/= Q[3] #diving by w
        points3d[count,:]=Q[:]
    return points3d


P1 = np.eye(4)
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

print(get3dPoints([P1,P2],[a3xN,b3xN]))


if __name__ == "__main__":
    pass