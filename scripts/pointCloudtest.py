
import numpy as np
import open3d as o3d


np_points=np.array([[0.0,0.0,0.0],[0.0,1.0,0.0],[1.0,0.0,0.0]])
np_colors=np.array([[255,255,0.0],[0.0,255,0.0],[0.0,0.0,255]])


pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(np_points)
pcd.colors=o3d.utility.Vector3dVector(np_colors)
o3d.io.write_point_cloud("sync.ply", pcd)

# Load saved point cloud and visualize it
pcd_load = o3d.io.read_point_cloud("sync.ply")
o3d.visualization.draw_geometries([pcd_load])


