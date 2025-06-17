#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2

class MapSaver(Node):
    def __init__(self):
        super().__init__('map_saver')
        self.sub = self.create_subscription(PointCloud2, '/map_points', self.callback, 10)
        self.all_points = []

    def callback(self, msg):
        points = list(pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True))
        # self.all_points.extend(points)
        self.all_points = points
        self.get_logger().info(f"Accumulated {len(self.all_points)} total points...")

    def save_to_pcd(self, filename="map_points.pcd"):
        with open(filename, "w") as f:
            f.write("# .PCD v0.7 - Point Cloud Data file format\n")
            f.write("VERSION 0.7\n")
            f.write("FIELDS x y z\n")
            f.write("SIZE 4 4 4\n")
            f.write("TYPE F F F\n")
            f.write("COUNT 1 1 1\n")
            f.write(f"WIDTH {len(self.all_points)}\n")
            f.write("HEIGHT 1\n")
            f.write("VIEWPOINT 0 0 0 1 0 0 0\n")
            f.write(f"POINTS {len(self.all_points)}\n")
            f.write("DATA ascii\n")
            for pt in self.all_points:
                f.write(f"{pt[0]} {pt[1]} {pt[2]}\n")
        self.get_logger().info(f"Saved accumulated point cloud to {filename}")

    def save_to_ply(self, filename="map_points.ply"):
        with open(filename, "w") as f:
            f.write("ply\n")
            f.write("format ascii 1.0\n")
            f.write(f"element vertex {len(self.all_points)}\n")
            f.write("property float x\n")
            f.write("property float y\n")
            f.write("property float z\n")
            f.write("end_header\n")
            for pt in self.all_points:
                f.write(f"{pt[0]} {pt[1]} {pt[2]}\n")
        self.get_logger().info(f"Saved accumulated point cloud to {filename}")

def main():
    rclpy.init()
    node = MapSaver()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.save_to_pcd()
        node.save_to_ply()
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()




# #!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import PointCloud2
# import sensor_msgs_py.point_cloud2 as pc2

# class MapSaver(Node):
#     def __init__(self):
#         super().__init__('map_saver')
#         self.sub = self.create_subscription(PointCloud2, '/map_points', self.callback, 10)
#         self.once = False

#     # def callback(self, msg):
#     #     if self.once:
#     #         return
#     #     self.once = True

#     #     self.get_logger().info('Received point cloud, saving...')

#     #     points = list(pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True))

#     #     with open("map_points.pcd", "w") as f:
#     #         # Write PCD header
#     #         f.write("# .PCD v0.7 - Point Cloud Data file format\n")
#     #         f.write("VERSION 0.7\n")
#     #         f.write("FIELDS x y z\n")
#     #         f.write("SIZE 4 4 4\n")
#     #         f.write("TYPE F F F\n")
#     #         f.write("COUNT 1 1 1\n")
#     #         f.write(f"WIDTH {len(points)}\n")
#     #         f.write("HEIGHT 1\n")
#     #         f.write("VIEWPOINT 0 0 0 1 0 0 0\n")
#     #         f.write(f"POINTS {len(points)}\n")
#     #         f.write("DATA ascii\n")
#     #         for pt in points:
#     #             f.write(f"{pt[0]} {pt[1]} {pt[2]}\n")

#     #     self.get_logger().info("Saved map_points.pcd")

#     def callback(self, msg):
#         if self.once:
#             return
#         self.once = True

#         self.get_logger().info('Received point cloud, saving...')
#         print(f"Timestamp: {msg.header.stamp.sec}.{msg.header.stamp.nanosec}")  # ← Add this line

#         points = list(pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True))

#         with open("map_points.pcd", "w") as f:
#             # Write PCD header
#             f.write("# .PCD v0.7 - Point Cloud Data file format\n")
#             f.write("VERSION 0.7\n")
#             f.write("FIELDS x y z\n")
#             f.write("SIZE 4 4 4\n")
#             f.write("TYPE F F F\n")
#             f.write("COUNT 1 1 1\n")
#             f.write(f"WIDTH {len(points)}\n")
#             f.write("HEIGHT 1\n")
#             f.write("VIEWPOINT 0 0 0 1 0 0 0\n")
#             f.write(f"POINTS {len(points)}\n")
#             f.write("DATA ascii\n")
#             for pt in points:
#                 f.write(f"{pt[0]} {pt[1]} {pt[2]}\n")

#         self.get_logger().info("Saved map_points.pcd")

# def main():
#     rclpy.init()
#     node = MapSaver()
#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         pass
#     node.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()
