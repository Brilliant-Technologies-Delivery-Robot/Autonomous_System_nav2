#!/usr/bin/python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ImageSubscriberPublisher(Node):
    def __init__(self):
        super().__init__('image_subscriber_publisher')

        # Create a subscriber to the /camera/camera/color/image_raw topic
        self.image_subscriber = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.image_callback,
            10
        )

        # Create a publisher to the /camera/color/image_published topic
        self.image_publisher = self.create_publisher(
            Image,
            '/camera/color/image_published',
            10
        )

        # Initialize CvBridge to convert ROS Image messages to OpenCV images
        self.bridge = CvBridge()

    def image_callback(self, msg):
        # Convert the ROS Image message to an OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        # Optionally, display the image using OpenCV (for debugging)
        cv2.imshow("Received Image", cv_image)
        cv2.waitKey(1)

        # Convert the OpenCV image back to a ROS Image message
        ros_image = self.bridge.cv2_to_imgmsg(cv_image, 'bgr8')
        self.image_publisher.publish(ros_image)
        self.get_logger().info('Published image to /camera/color/image_published')

def main(args=None):
    rclpy.init(args=args)
    # Create the node
    node = ImageSubscriberPublisher()
    # Spin the node to keep it alive and processing callbacks
    rclpy.spin(node)
    # Shutdown the node when done
    rclpy.shutdown()

if __name__ == '__main__':
    main()
