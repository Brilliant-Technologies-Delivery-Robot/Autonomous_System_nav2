import os
import launch
import launch_ros
from launch.substitutions import Command, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from ament_index_python import get_package_prefix
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    robotName = 'Robot1'
    namePackage = 'nav2'

    # Paths to URDF, RViz config, and world
    urdfModelPath = os.path.join(get_package_share_directory(namePackage), './src/description/urdf_assem.urdf')
  #  worldPath = os.path.join(get_package_share_directory(namePackage), 'worlds/neighborhood.world')
    worldPath = os.path.join(get_package_share_directory(namePackage), 'worlds/turtlebot3_world.world')
    rvizConfigPath = os.path.join(get_package_share_directory(namePackage), 'rviz', 'urdf_config2.rviz')
    ekfConfigPath = os.path.join(get_package_share_directory(namePackage), 'config', 'ekf.yaml')
  
    with open(urdfModelPath, 'r') as infp:
        robot_desc = infp.read()

    params = {'robot_description': robot_desc, 'use_sim_time': True}
       
    pkg_share_path = os.pathsep + os.path.join(get_package_prefix(namePackage), 'share')
    if 'GAZEBO_MODEL_PATH' in os.environ:
        os.environ['GAZEBO_MODEL_PATH'] += pkg_share_path
    else:
        os.environ['GAZEBO_MODEL_PATH'] = pkg_share_path
       
    gazebo_rosPackageLaunch = PythonLaunchDescriptionSource(
        os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
    )
    
    gazeboLaunch = IncludeLaunchDescription(
        gazebo_rosPackageLaunch,
        launch_arguments={'world': worldPath}.items()
    )
    
    spawnModelNode = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', robotName,'-x', '-2.0', '-y', '0', '-z', '0','-Y', '-1.5708' ],
        output='screen'
    )
    
    # Nodes
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )
    
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[params],
        condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    )

    # joint_state_publisher_gui_node = launch_ros.actions.Node(
    #     package='joint_state_publisher_gui',
    #     executable='joint_state_publisher_gui',
    #     name='joint_state_publisher_gui',
    #     condition=launch.conditions.IfCondition(LaunchConfiguration('gui'))
    # )
    
    # rviz_node = launch_ros.actions.Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     name='rviz2',
    #     output='screen',
    #     arguments=['-d', rvizConfigPath]  # Pass the RViz config file
    # )
    
    # # Robot Localization Node
    # robot_localization_node = launch_ros.actions.Node(
    #     package='robot_localization',
    #     executable='ekf_node',
    #     name='ekf_filter_node',
    #     output='screen',
    #     parameters=[ekfConfigPath,{'use_sim_time': True}]
    # )

    # Launch description  
    launchDescriptionObject = LaunchDescription()
    launchDescriptionObject.add_action(gazeboLaunch)
    launchDescriptionObject.add_action(spawnModelNode)
    launchDescriptionObject.add_action(robot_state_publisher_node)
    launchDescriptionObject.add_action(joint_state_publisher_node)
    # launchDescriptionObject.add_action(rviz_node)
    # launchDescriptionObject.add_action(robot_localization_node)
    return launchDescriptionObject
