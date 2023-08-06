import open3d as o3d

def custom_draw_geometry_with_rotation(pcd):

    def rotate_view(vis):
        ctr = vis.get_view_control()
        ctr.rotate(10.0, 0.0)
        return False

    o3d.visualization.draw_geometries_with_animation_callback([pcd], rotate_view)

def main():
    ply_point_cloud = o3d.data.PLYPointCloud()
    pcd = o3d.io.read_point_cloud(ply_point_cloud.path)
    custom_draw_geometry_with_rotation(pcd)

if __name__=="__main__":
    main()
