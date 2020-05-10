
import numpy as np
import open3d as o3d


#np_points=np.array([[0.0,0.0,0.0],[0.0,1.0,0.0],[1.0,0.0,0.0]])
#np_colors=np.array([[255,255,0.0],[0.0,255,0.0],[0.0,0.0,255]])
c1=np.load("data/3Dpoints/" + "0" + '.npy')
c2=np.load("data/3Dpoints/" + "1" + '.npy')
c3=np.load("data/3Dpoints/" + "2" + '.npy')
total=np.concatenate((c1,c2,c3),axis=0)

np_color=np.empty((total.shape))
for x in range(0,len(total)):
    if x >= 0 and x < len(c1):
        np_color[x]=[0.0,255,255]

    if x >= len(c1) and x < (len(c1)+len(c2)):
        np_color[x] = [255, 0.0, 255]

    if x >= (len(c1)+len(c2)) and x <= (len(c1)+len(c2)+len(c3)):
        np_color[x] = [0.0, 0.0, 0.0]

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(total)
pcd.colors=o3d.utility.Vector3dVector(np_color)
o3d.io.write_point_cloud("data/pointClouds/test.ply", pcd)

# Load saved point cloud and visualize it
pcd_load = o3d.io.read_point_cloud("data/pointClouds/test.ply")
o3d.visualization.draw_geometries([pcd_load])


