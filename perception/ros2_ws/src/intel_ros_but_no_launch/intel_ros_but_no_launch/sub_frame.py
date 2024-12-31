#!/usr/bin/python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')

        # Create a subscriber for the published image topic
        self.subscription = self.create_subscription(
            Image,
            '/camera/color/image_raw',
            self.image_callback,
            10  # QoS history depth
        )

        # Initialize CvBridge for ROS-OpenCV conversion
        self.bridge = CvBridge()

        self.get_logger().info('Subscribed to /camera/color/image_raw')

    def image_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

            # Display the image
            cv2.imshow("Published Image", cv_image)
            cv2.waitKey(1)  # Needed to update the OpenCV window

        except Exception as e:
            self.get_logger().error(f'Error displaying image: {e}')

def main(args=None):
    rclpy.init(args=args)

    # Create and spin the ImageSubscriber node
    node = ImageSubscriber()
    rclpy.spin(node)

    # Shutdown the node
    rclpy.shutdown()

if __name__ == '__main__':
    main()
