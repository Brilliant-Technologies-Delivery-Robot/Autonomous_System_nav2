#!/usr/bin/python3
import pyrealsense2 as rs
import numpy as np
import cv2

# Create a pipeline
pipeline = rs.pipeline()

# Configure the pipeline to stream depth, color, and infrared (left and right) streams
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)  # IR Left
config.enable_stream(rs.stream.infrared, 2, 640, 480, rs.format.y8, 30)  # IR Right

# Start the pipeline
pipeline.start(config)

# Check if GPU is available
if cv2.cuda.getCudaEnabledDeviceCount() == 0:
    print("No GPU found. GPU acceleration will not be used.")
else:
    print("GPU found. Using GPU acceleration.")

try:
    while True:
        # Wait for a new set of frames
        frames = pipeline.wait_for_frames()

        # Get individual frames
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        ir_left_frame = frames.get_infrared_frame(1)  # IR Left
        ir_right_frame = frames.get_infrared_frame(2)  # IR Right

        # Validate that all frames are available
        if not depth_frame or not color_frame or not ir_left_frame or not ir_right_frame:
            continue

        # Convert frames to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        ir_left_image = np.asanyarray(ir_left_frame.get_data())
        ir_right_image = np.asanyarray(ir_right_frame.get_data())

        # Apply GPU accelerated image processing (e.g., CUDA for color-to-grayscale conversion)
        if cv2.cuda.getCudaEnabledDeviceCount() > 0:
            # Convert color image to grayscale on GPU
            gpu_color = cv2.cuda_GpuMat()
            gpu_color.upload(color_image)
            gpu_gray = cv2.cuda.cvtColor(gpu_color, cv2.COLOR_BGR2GRAY)

            # Download the result back to CPU memory
            gray_image = gpu_gray.download()

            # Apply a filter or any other GPU operation (for example, a Gaussian blur)
            gpu_blur = cv2.cuda.GaussianBlur(gpu_gray, (5, 5), 0)
            blurred_image = gpu_blur.download()

            # You can now use the `blurred_image` for display or further processing
        else:
            # If no GPU is available, process on CPU
            gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
            blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

        # Apply colormap to depth image for better visualization
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Add captions to each image
        cv2.putText(color_image, 'Color Image', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(depth_colormap, 'Depth Image', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(ir_left_image, 'Infrared Left', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2, cv2.LINE_AA)
        cv2.putText(ir_right_image, 'Infrared Right', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2, cv2.LINE_AA)

        # Display each stream in its own window
        cv2.imshow('Color Stream', color_image)
        cv2.imshow('Depth Stream', depth_colormap)
        cv2.imshow('Infrared Left Stream', ir_left_image)
        cv2.imshow('Infrared Right Stream', ir_right_image)

        # Press 'q' or 'esc' to exit
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    # Stop the pipeline
    pipeline.stop()
