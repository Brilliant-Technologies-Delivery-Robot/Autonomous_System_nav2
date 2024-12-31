#!/usr/bin/python3

## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

#####################################################
##              Stream Infrared Image              ##
#####################################################

# Import the necessary libraries
import pyrealsense2 as rs
import numpy as np
import cv2

# Create a pipeline
pipeline = rs.pipeline()

# Configure the pipeline to stream IR frames
config = rs.config()

# Enable the infrared stream (default resolution and format)
# You can adjust the resolution and frame rate as needed
config.enable_stream(rs.stream.infrared, 640, 480, rs.format.y8, 30)

# Start the pipeline
pipeline.start(config)

# Streaming loop
try:
    while True:
        # Wait for a new set of frames
        frames = pipeline.wait_for_frames()

        # Get the infrared frame
        ir_frame = frames.get_infrared_frame()

        # Validate the frame
        if not ir_frame:
            continue

        # Convert the frame to a numpy array
        ir_image = np.asanyarray(ir_frame.get_data())

        # Display the infrared image
        cv2.namedWindow('Infrared Stream', cv2.WINDOW_NORMAL)
        cv2.imshow('Infrared Stream', ir_image)

        # Press 'q' or 'esc' to exit
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    # Stop the pipeline
    pipeline.stop()
