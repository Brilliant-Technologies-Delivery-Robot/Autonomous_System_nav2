#!/usr/bin/python3

import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()

# Enable depth and color streams
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Get the depth sensor's depth scale
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is:", depth_scale)

# Create an align object
align_to = rs.stream.color
align = rs.align(align_to)

# Define the point (x, y) in the image
x, y = 320, 240  # Example: center of the image

try:
    while True:
        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        # Get aligned depth and color frames
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue

        # Get depth image
        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Get the depth at the specific point (x, y)
        depth_at_point = depth_image[y, x] * depth_scale  # Depth value in meters

        # Print the depth at the point
        print(f"Depth at point ({x}, {y}): {depth_at_point} meters")

        # Visualize the color image with a circle at the (x, y) point
        cv2.circle(color_image, (x, y), 5, (0, 0, 255), -1)
        cv2.putText(color_image, f"Depth: {depth_at_point:.2f} m", (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the color image with the depth information
        cv2.imshow('Color Image', color_image)

        # Break the loop if 'q' is pressed
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
finally:
    pipeline.stop()
    cv2.destroyAllWindows()
