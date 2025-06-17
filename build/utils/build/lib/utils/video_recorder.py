import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np
import cv2

class VideoRecorder(Node):
    def __init__(self):
        super().__init__('video_recorder')
        self.subscription = self.create_subscription(
            Image,
            '/camera_main/image_raw',
            self.listener_callback,
            10)

        self.writer = None
        self.fps = 30  # Adjust as needed
        self.output_file = 'camera_raw_output.mp4'

    def listener_callback(self, msg):
        # Only support RGB8 or BGR8 for now
        if msg.encoding not in ['rgb8', 'bgr8']:
            self.get_logger().error(f"Unsupported encoding: {msg.encoding}")
            return

        dtype = np.uint8
        channels = 3  # RGB/BGR
        image_np = np.frombuffer(msg.data, dtype=dtype).reshape((msg.height, msg.width, channels))

        # Convert to BGR for OpenCV if needed
        if msg.encoding == 'rgb8':
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        if self.writer is None:
            self.writer = cv2.VideoWriter(
                self.output_file,
                cv2.VideoWriter_fourcc(*'mp4v'),
                self.fps,
                (msg.width, msg.height)
            )
            self.get_logger().info(f"Started recording to {self.output_file}")

        self.writer.write(image_np)

    def destroy_node(self):
        if self.writer:
            self.writer.release()
            self.get_logger().info("Video saved.")
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    recorder = VideoRecorder()

    try:
        rclpy.spin(recorder)
    except KeyboardInterrupt:
        pass
    finally:
        recorder.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
