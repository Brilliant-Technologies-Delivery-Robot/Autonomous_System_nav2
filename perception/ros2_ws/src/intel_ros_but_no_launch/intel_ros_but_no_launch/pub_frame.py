#!/usr/bin/python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import pyrealsense2 as rs
import cv2
import numpy as np

class RealSensePublisher(Node):
    def __init__(self):
        super().__init__('realsense_publisher')

        # Create a publisher for the RGB frames
        self.publisher = self.create_publisher(Image, '/camera/color/image_raw', 10)

        # Initialize CvBridge for ROS-OpenCV conversion
        self.bridge = CvBridge()

        # Configure the RealSense pipeline
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        # Enable the color stream (RGB)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start the RealSense pipeline
        self.pipeline.start(self.config)
        self.get_logger().info('RealSense pipeline started.')

        # Create a timer to publish frames at a fixed rate
        self.timer = self.create_timer(1 / 30, self.publish_frame)  # 30 FPS

    def publish_frame(self):
        try:
            # Wait for a frame from the RealSense camera
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()

            if not color_frame:
                self.get_logger().warn('No color frame available.')
                return

            # Convert the RealSense frame to a numpy array
            color_image = np.asanyarray(color_frame.get_data())

            # Convert the numpy array to a ROS Image message
            ros_image = self.bridge.cv2_to_imgmsg(color_image, encoding='bgr8')

            # Publish the ROS Image message
            self.publisher.publish(ros_image)
            self.get_logger().info('Published a color frame.')

        except Exception as e:
            self.get_logger().error(f'Error capturing or publishing frame: {e}')

def main(args=None):
    rclpy.init(args=args)

    # Create and spin the RealSensePublisher node
    node = RealSensePublisher()
    rclpy.spin(node)

    # Shutdown the node and stop the pipeline
    node.pipeline.stop()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
