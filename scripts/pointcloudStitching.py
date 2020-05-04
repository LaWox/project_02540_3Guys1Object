import open3d
import cv2
import numpy as np
import copy
import open3d as o3d

pointcloud1 = o3d.io.read_point_cloud('pointClouds/cloud1.ply')
pointcloud2 = o3d.io.read_point_cloud('pointClouds/cloud2.ply')

def stitch2Pointclouds(cloud1, cloud2, )



def drawRegistrations(source, target, transformation = None, recolor = false):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
