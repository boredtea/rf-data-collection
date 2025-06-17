#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import sensor_msgs_py.point_cloud2 as pc2

class FinalMapSaver(Node):
    def __init__(self):
        super().__init__('final_map_saver')
        self.sub = self.create_subscription(PointCloud2, '/map_points', self.callback, 10)
        self.latest_points = []
        self.get_logger().info("Listening for /map_points...")

    def callback(self, msg):
        # Just overwrite with the latest message's points
        self.latest_points = list(pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True))
        self.get_logger().info(f"Updated map with {len(self.latest_points)} points")

    def save_to_ply(self, filename="final_map_points.ply"):
        if not self.latest_points:
            self.get_logger().warn("No points received, not saving.")
            return

        with open(filename, "w") as f:
            f.write("ply\n")
            f.write("format ascii 1.0\n")
            f.write(f"element vertex {len(self.latest_points)}\n")
            f.write("property float x\n")
            f.write("property float y\n")
            f.write("property float z\n")
            f.write("end_header\n")
            for pt in self.latest_points:
                f.write(f"{pt[0]} {pt[1]} {pt[2]}\n")

        self.get_logger().info(f"Saved final map to {filename}")

def main():
    rclpy.init()
    node = FinalMapSaver()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.save_to_ply()

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
