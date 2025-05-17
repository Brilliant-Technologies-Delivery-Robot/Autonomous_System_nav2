# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import yaml
import launch_ros.actions
from ament_index_python.packages import get_package_share_directory
from launch.actions import ExecuteProcess
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml



def generate_launch_description():

   ld = LaunchDescription()

   map_file_path = os.path.join(
   get_package_share_directory('amcl2'),
    'maps',
    'turtlebot3_world.yaml'
    )
    # Get the launch directory
   bringup_dir = get_package_share_directory('amcl2')

   namespace = LaunchConfiguration('namespace')
    #map_yaml_file = LaunchConfiguration('map')
   use_sim_time = LaunchConfiguration('use_sim_time')
   autostart = LaunchConfiguration('autostart')
   params_file = LaunchConfiguration('params_file')
   lifecycle_nodes = ['map_server', 'amcl']

    # Map fully qualified names to relative ones so the node's namespace can be prepended.
    # In case of the transforms (tf), currently, there doesn't seem to be a better alternative
    # https://github.com/ros/geometry2/issues/32
    # https://github.com/ros/robot_state_publisher/pull/30
    # TODO(orduno) Substitute with `PushNodeRemapping`
    #              https://github.com/ros2/launch_ros/issues/56
   remappings = [('/tf', 'tf'),
                  ('/tf_static', 'tf_static')]

    # Create our own temporary YAML files that include substitutions
   param_substitutions = {
         'use_sim_time': use_sim_time,
         'yaml_filename': map_file_path}

   configured_params = RewrittenYaml(
         source_file=params_file,
         root_key=namespace,
         param_rewrites=param_substitutions,
         convert_types=True)
         
   map_server_cmd=Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            namespace=namespace,
            parameters=[{'yaml_filename': map_file_path}],
            remappings=remappings),
   start_lifecycle_manager_cmd = launch_ros.actions.Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_localization',
            output='screen',
            namespace=namespace,
            parameters=[{'use_sim_time': use_sim_time},
                        {'autostart': autostart},
                        {'node_names': lifecycle_nodes}])
    
   ld.add_action(map_server_cmd)
   ld.add_action(start_lifecycle_manager_cmd)
   return LaunchDescription([
        # Set env var to print messages to stdout immediately
        SetEnvironmentVariable('RCUTILS_LOGGING_BUFFERED_STREAM', '1'),

        DeclareLaunchArgument(
            'namespace', default_value='',
            description='Top-level namespace'),

        DeclareLaunchArgument(
            'map',
            default_value=os.path.join('amcl2', 'maps', 'turtlebot3_world.yaml'),
            description='Full path to map yaml file to load'),

        DeclareLaunchArgument(
            'use_sim_time', default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        DeclareLaunchArgument(
            'autostart', default_value='true',
            description='Automatically startup the nav2 stack'),

        DeclareLaunchArgument(
            'params_file',
            default_value=os.path.join(bringup_dir, 'params', 'amcl.yaml'),
            description='Full path to the ROS2 parameters file to use'),

  

        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            namespace=namespace,
            parameters=[configured_params],
            remappings=remappings),])  
            
            

     
