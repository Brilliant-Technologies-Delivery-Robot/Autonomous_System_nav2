#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import yaml
import numpy as np
import cv2
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Pose
from std_msgs.msg import Header


class MapPublisher(Node):
    def __init__(self, map_yaml_path):
        super().__init__("map_publisher")
        self.publisher = self.create_publisher(OccupancyGrid, "map", 10)
        self.timer = self.create_timer(1.0, self.publish_map)  # Publish every second

        # Load map data
        self.map_metadata, self.map_data = self.load_map(map_yaml_path)
        self.get_logger().info("Map loaded successfully! Publishing on /map topic")

    def load_map(self, yaml_path):
        """Loads map metadata and image data from .yaml and .pgm files."""
        with open(yaml_path, "r") as yaml_file:
            map_metadata = yaml.safe_load(yaml_file)

        pgm_path = map_metadata["image"]
        if not pgm_path.startswith("/"):  # Convert relative path to absolute
            import os
            pgm_path = os.path.join(os.path.dirname(yaml_path), pgm_path)

        # Load PGM image
        image = cv2.imread(pgm_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            self.get_logger().error(f"Failed to load map image: {pgm_path}")
            exit(1)

        # Extract dimensions from image (Fix for missing width/height)
        map_metadata["width"] = image.shape[1]  # X-dimension (columns)
        map_metadata["height"] = image.shape[0]  # Y-dimension (rows)

        self.get_logger().info(f"Loaded map metadata: {map_metadata}")

        # Convert PGM to OccupancyGrid format
        occupancy_grid = self.convert_pgm_to_grid(image, map_metadata)
        return map_metadata, occupancy_grid

    def convert_pgm_to_grid(self, image, metadata):
        """Converts a PGM image into an OccupancyGrid format."""
        image = np.flipud(image)  # Flip image vertically to match ROS coordinate system
        occupancy_grid = np.zeros(image.shape, dtype=np.int8)

        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                pixel_value = image[y, x]
                if pixel_value == 205:  # Unknown
                    occupancy_grid[y, x] = -1
                elif pixel_value == 0:  # Occupied (black)
                    occupancy_grid[y, x] = 100
                else:  # Free space (white)
                    occupancy_grid[y, x] = 0

        return occupancy_grid.flatten().tolist()

    def publish_map(self):
        """Publishes the OccupancyGrid message."""
        msg = OccupancyGrid()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "map"

        # Set map metadata
        msg.info.resolution = self.map_metadata["resolution"]
        msg.info.width = self.map_metadata["width"]
        msg.info.height = self.map_metadata["height"]

        msg.info.origin = Pose()
        msg.info.origin.position.x = self.map_metadata["origin"][0]
        msg.info.origin.position.y = self.map_metadata["origin"][1]
        msg.info.origin.position.z = 0.0
        msg.info.origin.orientation.w = 1.0  # No rotation

        msg.data = self.map_data
        self.publisher.publish(msg)
        self.get_logger().info("Published map!")

def main(args=None):
    rclpy.init(args=args)
    node = MapPublisher("/home/alaa/ros2_ws/src/Autonomous_System_nav2/slam/amcl2/maps/turtlebot3_world.yaml")  # Update with your actual file path
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

