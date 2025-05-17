# ROS 2 - ros2_odom_subscriber.py

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

class OdomSubscriber(Node):
    def __init__(self):
        super().__init__('ros2_odom_subscriber')
        self.subscription = self.create_subscription(
            Odometry,
            '/hoverboard_velocity_controller/odom',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        position = msg.pose.pose.position
        self.get_logger().info(
            f'Received Odometry -> Position: x={position.x}, y={position.y}, z={position.z}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = OdomSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

