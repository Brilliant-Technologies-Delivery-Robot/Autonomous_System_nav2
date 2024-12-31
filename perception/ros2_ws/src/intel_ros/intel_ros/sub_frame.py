#!/usr/bin/python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')

        # Initialize CvBridge to convert ROS Image messages to OpenCV images
        self.bridge = CvBridge()

        # Create a subscriber to the /camera/camera/color/image_raw topic
        self.image_subscriber = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.image_callback,
            10  # QoS history depth
        )

        self.get_logger().info('Subscribed to /camera/camera/color/image_raw')

    def image_callback(self, msg):
        # Convert the ROS Image message to an OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        # Convert the image to grayscale
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Display the grayscale image
        cv2.imshow("Grayscale Image", gray_image)
        cv2.waitKey(1)  # Display the image for 1ms (needed for OpenCV to update the window)

        # Optionally, print image metadata (can be removed if not needed)
        self.get_logger().info(f'Received image: {msg.width}x{msg.height}, encoding: {msg.encoding}')

def main(args=None):
    rclpy.init(args=args)

    # Create the node
    node = ImageSubscriber()

    # Spin the node to keep it alive and processing callbacks
    rclpy.spin(node)

    # Shutdown the node when done
    rclpy.shutdown()

if __name__ == '__main__':
    main()
