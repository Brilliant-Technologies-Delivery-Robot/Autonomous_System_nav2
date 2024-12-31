import pyrealsense2 as rs
import cv2
import numpy as np

# Configure the pipeline to stream RGB frames
pipeline = rs.pipeline()
config = rs.config()

# Enable the color stream (RGB)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start the pipeline
pipeline.start(config)

try:
    while True:
        # Wait for a coherent pair of frames: color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Convert the color frame to a numpy array
        color_image = np.asanyarray(color_frame.get_data())

        # Display the RGB frame
        cv2.imshow('RealSense RGB Stream', color_image)

        # Exit the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Stop the pipeline
    pipeline.stop()
    cv2.destroyAllWindows()
