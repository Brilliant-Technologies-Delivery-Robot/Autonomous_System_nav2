# Overview
This workspace mainly developed to work with ros2-foxy but need to be built first. it contians the package developed by intel itself and trivial package to receive frame and publish it and apply filter over it.

# Files
In the src files there's three main files which are ros packages. we need to talk about.
## realsense-ros
This file is developed with **intel** and we can get it by following the below link.
```bash
https://github.com/IntelRealSense/realsense-ros?tab=readme-ov-file
```
The link above provides several things. launch files that publishes depth images , point clouds .. etc. also it contains the urdf and familiar things like that.

## intel_ros
This files we have two python files one of them subscribes from the cameras topic that published after writting the below in the terminal.
```bash
ros2 launch realsense2_camera rs_launch.py enable_rgbd:=true enable_sync:=true align_depth.enable:=true enable_color:=true enable_depth:=true 
```
After launching the above launch file i have made up a subscriber that subs to the topic **/camera/camera/color/image_raw** and then publishes it again to another topic.

## intel_ros_but_no_launch
The same as **intel_ros** but we don't have to run the launch file above. and this is the same for depth clouds and point clouds here. unlike the kinect camera.