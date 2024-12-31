# Project Overview

This file mainly concerned with some code trials with **IntelRealSenseD435i**. 
## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [File Descriptions](#descriptions)

## Introduction

Several python codes to be familiar with the intelrealsensed435i camera and the stearming. the codes are maded with the help of the **intelrealsense SDK wrapper python examples**.

## Installation

### Prerequisites

List any software or libraries needed to run the project (e.g., Python, ROS, dependencies).

- Python 3.x
- OpenCV
- pyrealsense2

To download them. 
```bash
pip install opencv-python
pip install pyrealsense2
```

## File Descriptions

### `stream_rgb.py`
This script handles streaming of RGB images from the camera. It captures and processes RGB frames, providing real-time access to the camera feed.

### `stream_ir.py`
This script is responsible for streaming infrared (IR) images. It captures IR frames from the camera, enabling depth perception and thermal data capture.

### `stream_point_cloud.py`
This script streams point cloud data, which represents 3D spatial data collected by the camera. It allows for 3D visualization and analysis of the environment.

### `stream_depth_image.py`
This script streams depth images, providing the distance from the camera to various objects in the scene. It is essential for depth perception and 3D scene reconstruction.

### `stream_all_avail.py`
This script streams all available data from the camera, including RGB, IR, depth, and point cloud, providing a comprehensive view of the captured environment.

### `depth_and_rgb_alignment.py`
This script aligns depth and RGB images, ensuring that both datasets are synchronized and can be used together for tasks such as object detection or 3D reconstruction.

### `depth_at_cursor_pos.py`
This script retrieves the depth value at the position of the cursor in the RGB image. It is useful for interactive depth measurements or point selection in a 3D space.

### `depth_at_point.py`
This script provides the depth value at a specific point in the depth image. It allows users to extract depth information at any given pixel location.

### `depth2image_alignment.py`
This script aligns depth data with the corresponding RGB image, ensuring that depth information is accurately mapped to its visual counterpart in the RGB feed.
