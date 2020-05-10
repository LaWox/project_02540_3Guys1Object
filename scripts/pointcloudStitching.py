import open3d
import cv2
import numpy as np
import copy
import open3d as o3d


def drawRegistrations(source, target, transformation = None, recolor = False):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)

    if recolor:
        source_temp.paint_uniform_color([1, 0.701, 0])
        target_temp.paint_uniform_color([0, 0.651, 0.929])
    if (transformation is not None):
        source_temp.transform(transformation)
    o3d.visualization.draw_geometries([source_temp, target_temp])

    return  None


def globalRegistration(source, target, voxel_size = 0.05, ):

    source_sample = source.voxel_down_sample(voxel_size)
    target_sample = target.voxel_down_sample(voxel_size)

    source_sample.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius = 2 * voxel_size, max_nn = 100))
    target_sample.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius = 2 * voxel_size, max_nn = 100))

    source_fpfh = o3d.registration.compute_fpfh_feature(source_sample, o3d.geometry.KDTreeSearchParamHybrid(radius = 2 * voxel_size, max_nn = 100))
    target_fpfh = o3d.registration.compute_fpfh_feature(target_sample, o3d.geometry.KDTreeSearchParamHybrid(radius=2 * voxel_size, max_nn=100))

    point_to_point = o3d.io.registration.TransformationEstimationPointToPoint(False)
    distance_threshold = 1.5*voxel_size
    corr_check = [o3d.registration.CorrespondenceCheckerBasedOnDistance(distance_threshold)]

    ransac_result = o3d.registration.registration_ransac_based_on_feature_matching(source_sample, target_sample, source_fpfh, target_fpfh,
                                                                                   distance_threshold, point_to_point, checkers = corr_check)
    return ransac_result


cld1 = o3d.io.read_point_cloud("data/3D_point_cloud_test/r1.pcd")
cld2 = o3d.io.read_point_cloud("data/3D_point_cloud_test/r2.pcd")

ransac_result = globalRegistration(cld1, cld2, 0.05)
trans = ransac_result.transformation

drawRegistrations(cld1, cld2, trans, True)

def ICP(source, target, ):

    #Evaluate initial alignment
    threshold = 0.02
    trans
