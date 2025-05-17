import os


from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.conditions import UnlessCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from nav2_common.launch import HasNodeParams


def generate_launch_description():


    default_params_file = os.path.join(get_package_share_directory("slam"),
                                       'config', 'mapper_params_localization.yaml')
                                       
    start_localization_slam_toolbox_node = Node(
        parameters=[
           default_params_file,
          {'use_sim_time': False }
        ],
        package='slam_toolbox',
        executable='localization_slam_toolbox_node',
        name='slam_toolbox',
        output='screen')     
        
    ld = LaunchDescription()                            
                                
    ld.add_action(start_localization_slam_toolbox_node)


    return ld 
