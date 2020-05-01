import cv2

import camera



camera1 = camera.Camera("dd", "gg", calibrated=True)

k = camera1.getK()
print(k)

camera.objPoints

'''
def rectify_images(camera_rig, cameras, imagepath):
'''
