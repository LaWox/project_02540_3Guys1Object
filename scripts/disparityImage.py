import open3d as o3d
import cv2


def rectify_images(camera_rig, cameras, imagepath):

      for i in range(len(cameras)):
          for j in range(i+1, len(cameras)):


