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


def globalRegistration(source, target, voxel_size):
    #Checks for these correspondences in ransac loops
    corr_check = [o3d.registration.CorrespondenceCheckerBasedOnDistance(distance_threshold)]

    #Down sampling the point cloud for faster computation
    source_sample = source.voxel_down_sample(voxel_size)
    target_sample = target.voxel_down_sample(voxel_size)

    #Estimating the normals for each point in cloud, to use to find fpfh features
    source_sample.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius = 2 * voxel_size, max_nn = 100))
    target_sample.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius = 2 * voxel_size, max_nn = 100))

    #Finding the fpfh feature histograms
    source_fpfh = o3d.registration.compute_fpfh_feature(source_sample, o3d.geometry.KDTreeSearchParamHybrid(radius = 2 * voxel_size, max_nn = 100))
    target_fpfh = o3d.registration.compute_fpfh_feature(target_sample, o3d.geometry.KDTreeSearchParamHybrid(radius=2 * voxel_size, max_nn=100))

    #Defining the error measure for the registration by ransac
    point_to_point = o3d.registration.TransformationEstimationPointToPoint(False)
    distance_threshold = 1.5*voxel_size

    #The final result of transformation between the two pointclouds
    ransac_result = o3d.registration.registration_ransac_based_on_feature_matching(source_sample, target_sample, source_fpfh, target_fpfh,
                                                                                   distance_threshold, point_to_point, checkers = corr_check)
    return ransac_result


cld1 = o3d.io.read_point_cloud("/Users/william/PycharmProjects/project_02540_3Guys1Object/data/3D_point_cloud_test/r1.pcd")
cld2 = o3d.io.read_point_cloud("/Users/william/PycharmProjects/project_02540_3Guys1Object/data/3D_point_cloud_test/r1.pcd")

ransac_result = globalRegistration(cld1, cld2, 0.05)
trans = ransac_result.transformation

drawRegistrations(cld1, cld2, trans, True)

def ICP(source, target, threshold, rad, maxnn):
    #Initial transformation
    trans_init = np.asarray([[1, 0, 0, o], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    #Evaluate initial alignment?

    #Defining the error measure
    point_to_plane = o3d.registration.TransformationEstimationPointToPlane()

    #Estimating the normals for each point, to define planes in the point to plane algorithm
    source.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
        radius=rad, max_nn=maxnn), fast_normal_computation=True)
    target.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
        radius=rad, max_nn=maxnn), fast_normal_computation=True)

    icp_res = o3d.registration.registration_icp(source, target, threshold, trans_init, point_to_plane)

    return icp_res


#source_aligned =
#target_aligned =

icp_result = ICP(source_aligned, target_aligned, 0.1, 0.5, 300)

icp_trans = icp_result.transformation

#Source and target stitched together
Stitched = target + source.transform(icp_trans)
