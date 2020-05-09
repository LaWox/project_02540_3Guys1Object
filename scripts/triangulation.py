# Triangulering

import cv2 
import numpy as np
from camera import Camera
from cameraRig import Rig
from featureDetMatch import getMatches
from imageProcessing import rectifyImage, rectifyImageTest

#Kasta in bilderna också

"""def get3dPoints(pList, featuresList):
    #points3d=np.empty((int(np.floor(len(pList)/2)),len(featuresList),len(featuresList[0])))
    points3D=[]
    count=0
    for x in range(0,len(pList)-1):

        Q=cv2.triangulatePoints(pList[x],pList[x+1],featuresList[x],featuresList[x+1])
        Q/= Q[3] #diving by w

        #points3d[count]=Q[:]
        points3D.append(Q[:])
    return points3D"""

def get3dPointsUnrect(matches, rig):
    points3d = np.empty((len(matches),3))
    pointsColor = np.empty((len(matches),3))
    count=0

    # TODO: Fix how we get the projection matrix


    for x in range(0,len(matches)):
        cam1=matches[x].point1.camera.getCameraNo()
        cam2=matches[x].point2.camera.getCameraNo()
        coord1 = makeNestedList(matches[x].point1.getCoords())
        coord2 = makeNestedList(matches[x].point2.getCoords())

        Rt = rig.getRt(cam1,cam2)
        K1 = matches[x].point1.camera.getK()
        K2 = matches[x].point2.camera.getK()

        #P1=np.concatenate((K1,np.zeros((3,1))),axis=1)

        #P1=K1@np.eye(4)[:3]
        #P1=K1@Rt
        P1 = np.eye(4)[:3]
        P2=K2@Rt

        #Triangulation
        Q=cv2.triangulatePoints(P1,P2,coord1,coord2)
        #print(Q)
        Q/= Q[3] #diving by w
        #print(Q)

        points3d[count]=np.transpose(Q[:3])[0] #becomes a 3D vector, w is removed
        #print(points3d[count])

        #Storing the color
        #pointsColor[count]=matches[x].getColor()

        count +=1

    return [points3d, pointsColor]

def makeNestedList(list):
    newList = np.empty((len(list), 1))
    for x in range(0,len(list)):
        newList[x][0] = list[x]

    return newList


def get3dPointsRect(matches, rig):
    points3d = np.empty((len(matches),3))
    pointsColor = np.empty((len(matches),3))
    count=0

    # TODO: Fix how we get the projection matrix


    for x in range(0,len(matches)):
        cam1=matches[x].point1.camera.getCameraNo()
        cam2=matches[x].point2.camera.getCameraNo()
        coord1 = makeNestedList(matches[x].point1.getCoords())
        coord2 = makeNestedList(matches[x].point2.getCoords())

        P1 = rig.getProjectionTransformRectified(cam1,cam2)[0]
        P2 = rig.getProjectionTransformRectified(cam1,cam2)[1]
        #K1 = matches[x].point1.camera.getK()
        #P1 = K1 @ np.eye(4)[:3]

        #Triangulation
        Q=cv2.triangulatePoints(P1,P2,coord1,coord2)
        #print(Q)
        Q/= Q[3] #diving by w
        #print(Q)

        points3d[count]=np.transpose(Q[:3])[0] #becomes a 3D vector, w is removed
        #print(points3d[count])

        #Storing the color
        #pointsColor[count]=matches[x].getColor()

        count +=1

    return [points3d, pointsColor]

"""def getError(pList,featList, pointsL):
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

        count += 1"""

def getErrorRect(matches, pointsL, rig):
    count = 0
    error1 = 0.0
    error2 = 0.0
    for x in range(0,len(matches)):
        cam1 = matches[x].point1.camera.getCameraNo()
        cam2 = matches[x].point2.camera.getCameraNo()
        coord1 = matches[x].point1.getCoords()
        coord2 = matches[x].point2.getCoords()
        P1 = rig.getProjectionTransformRectified(cam1, cam2)[0]
        P2 = rig.getProjectionTransformRectified(cam1, cam2)[1]
        #K1 = matches[x].point1.camera.getK()
        #P1 = K1 @ np.eye(4)[:3]


        points3d = np.concatenate((pointsL[x], np.array([1])))
        points3d=makeNestedList(points3d)

        pixel1 = P1 @ points3d
        pixel1 /= pixel1[2]
        pixel2 = P2 @ points3d
        pixel2 /= pixel2[2]


        error1 += np.sqrt(np.sum((coord1 - pixel1[:2].flatten()) ** 2))
        error2 += np.sqrt(np.sum((coord2 - pixel2[:2].flatten()) ** 2))
        #print('Error in cam1',error1,'Error in cam2',error2)
        #sum += error1 + error2



        count += 1
    error1Mean = error1/count
    error2Mean = error2/count
    #return sum / count
    return [error1Mean,error2Mean]

def getErrorUnrect(matches, pointsL, rig):
    count = 0
    sum = 0.0
    error1 = 0.0
    error2 = 0.0
    for x in range(0,len(matches)):
        cam1 = matches[x].point1.camera.getCameraNo()
        cam2 = matches[x].point2.camera.getCameraNo()
        coord1 = matches[x].point1.getCoords()
        coord2 = matches[x].point2.getCoords()

        Rt = rig.getRt(cam1, cam2)
        K1 = matches[x].point1.camera.getK()
        K2 = matches[x].point2.camera.getK()

        #P1 = np.concatenate((K1, np.zeros((3, 1))), axis=1)
        #P1 = K1 @ np.eye(4)[:3]
        P1 = np.eye(4)[:3]
        #P1 = K1 @ Rt
        P2 = K2 @ Rt


        points3d = np.concatenate((pointsL[x], np.array([1])))
        points3d=makeNestedList(points3d)

        pixel1 = P1 @ points3d
        if (pixel1[2] == 0.0):
            pixel1[2] = 0.001
        pixel1 /= pixel1[2]


        pixel2 = P2 @ points3d
        if (pixel2[2] == 0.0):
            pixel2[2] = 0.001
        pixel2 /= pixel2[2]


        error1 += np.sqrt(np.sum((coord1 - pixel1[:2].flatten()) ** 2))
        error2 += np.sqrt(np.sum((coord2 - pixel2[:2].flatten()) ** 2))

        count += 1

    return [error1/count, error2/count]




"""P1 = np.eye(4)[:3]
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


getError([P1,P2],[a3xN,b3xN],points)"""




if __name__ == "__main__":



    calibrationPath1 = "data/cameraData/camera0/"
    calibrationPath2 = "data/cameraData/camera1/"
    calibrationPath3 = "data/cameraData/camera2/"
    objPath1 = "data/Pictures/Jussi/cornflakes_jussi_resized/"
    objPath2 = "data/Pictures/Platon/cornflakes_platon_resized/"
    objPath3 = "data/Pictures/William/cornflakes_william/"
    camera1 = Camera(calibrationPath1, objPath1, cameraNr = 0, calibrated=True)
    camera2 = Camera(calibrationPath2, objPath2, cameraNr = 1, calibrated=True)
    camera3 = Camera(calibrationPath3, objPath3, cameraNr = 2, calibrated=True)
    rig = Rig([camera1,camera2,camera3], calibrated=True)
    rig=rectifyImage(rig)
    rectList=rectifyImageTest(rig)

    cv2.cv2.namedWindow('01', cv2.WINDOW_NORMAL)
    cv2.imshow('01',rectList[0][0])
    cv2.resizeWindow('01', 500, 500)

    cv2.cv2.namedWindow('02', cv2.WINDOW_NORMAL)
    cv2.imshow('02', rectList[1][0])
    cv2.resizeWindow('02', 500, 500)

    cv2.cv2.namedWindow('12', cv2.WINDOW_NORMAL)
    cv2.imshow('12', rectList[2][0])
    cv2.resizeWindow('12', 500, 500)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    matches=getMatches(rig)
    pointList=[]

    for match in matches:
        print(len(match))
        points, color = get3dPointsRect(match,rig)
        pointList.append(points)

    sumV=np.empty((len(matches),2))
    for x in range(0,len(pointList)):
        errCam1, errCam2=getErrorRect(matches[x],pointList[x],rig)
        print('The average error in cam1', errCam1, 'The average error in cam2', errCam2)
        sumV[x]=np.array([errCam1,errCam2])
    print(sumV)
    print(np.mean(sumV))

    for x in range(0,len(pointList)):
        np.save(("data/3Dpoints/" + str(x)), pointList[x])





    print('Done')





    pass