import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os

def generate_launch_description():
    # Locate the package
    pkg_share = launch_ros.substitutions.FindPackageShare(package='nav2').find('nav2')

    # Paths to URDF and RViz config
    default_model_path = os.path.join(pkg_share, 'src/description/urdf_assem.urdf')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/urdf_config.rviz')

    # Nodes
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
        {'robot_description': launch_ros.descriptions.ParameterValue(
        open(default_model_path, 'r').read(), 
        value_type=str
        )}
        ]
    )
    
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        arguments=[default_model_path],
    )

    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
        output='screen'
    )

    spawn_entity = launch_ros.actions.Node(
    package='gazebo_ros',
    executable='spawn_entity.py',
    arguments=['-entity', 'urdf_assem', '-topic', 'robot_description'],
    output='screen'
    )

    # Launch description
    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            name='model', 
            default_value=default_model_path, 
            description='Absolute path to robot URDF file'
        ),
        launch.actions.DeclareLaunchArgument(
            name='rvizconfig', 
            default_value=default_rviz_config_path, 
            description='Absolute path to RViz config file'
        ),
        launch.actions.DeclareLaunchArgument(
            name='use_simulation', 
            default_value='False', 
            description='Flag to enable simulation in Gazebo'
        ),
        launch.actions.ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'], output='screen'),      
        joint_state_publisher_node,
        robot_state_publisher_node,
        spawn_entity,
        rviz_node
    ])
