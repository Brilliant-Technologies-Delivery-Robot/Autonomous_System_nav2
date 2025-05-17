import os

from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node



def generate_launch_description():

    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='navigation_control' 
    #namePackage = 'robot_urdf'
    robotName='version_0' 
    
    # ekfConfigPath = os.path.join(get_package_share_directory(namePackage), 'config', 'ekf.yaml')
    
    #controllers_yaml = os.path.join(get_package_share_directory(package_name), 'config', 'my_controllers.yaml')
   # world_path = os.path.join(get_package_share_directory(package_name), 'worlds/obstacles.world')
    #gazebo_params_path = os.path.join(get_package_share_directory(package_name), 'config/gazebo_params.yaml')
    rvizConfigPath = os.path.join(get_package_share_directory(package_name), 'rviz/rviz_config.rviz')
   # twist_mux_params = os.path.join(get_package_share_directory(package_name),'config','twist_mux.yaml')
    
    # urdf_path = os.path.join(get_package_share_directory(namePackage), 'description', 'robot_core.xacro')
    # robot_description = ParameterValue(
    # Command(['xacro ', urdf_path, ' ', 'use_ros2_control:=true']),
    # value_type=str)
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'false ', 'use_ros2_control': 'true'}.items()
    )
    
    
    # Include RPLIDAR Launch
    rplidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('rplidar_ros'), 'launch', 'rplidar_a1_launch.py')
        ),
    )

     #Include SLAM Toolbox Launch
    #slam_launch = IncludeLaunchDescription(
     #   PythonLaunchDescriptionSource(
      #      os.path.join(get_package_share_directory('slam'), 'launch', 'online_async_launch.py')
       # ),
        #launch_arguments={
         #   'use_sim_time': 'false',
          # 'params_file': os.path.join(get_package_share_directory('slam'), 'config', 'mapper_params_online_async.yaml')
        #}.items()
    #)
    
    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
           os.path.join(get_package_share_directory('slam'), 'launch', 'localization_launch.py')
       ),
       launch_arguments={
           'use_sim_time': 'false',
          'params_file': os.path.join(get_package_share_directory('slam'), 'config', 'mapper_params_localization.yaml')
        }.items()
   )
    
 #   amcl_launch = IncludeLaunchDescription(
  #      PythonLaunchDescriptionSource(
   #       os.path.join(get_package_share_directory('amcl2'), 'launch', 'map_server_delay.launch.py')
    #   )
   #)
    
    
                
    # Robot Localization Node
    # robot_localization_node = launch_ros.actions.Node(
    #     package='robot_localization',
    #     executable='ekf_node',
    #     name='ekf_filter_node',
    #     output='screen',
    #     parameters=[ekfConfigPath,{'use_sim_time': True}]
    # )

    # # Include the Gazebo launch file, provided by the gazebo_ros package
    # gazebo = IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(
    #                 get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    #             launch_arguments={
    #                 'world': world_path,
    #                 'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_path
    #             }.items()
    # )

    # # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    # spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
    #                     arguments=['-topic', 'robot_description',
    #                                '-entity', robotName,'-x', '0', '-y', '0', '-z', '0','-Y', '0' ],
    #                     output='screen'
    # )
    
    # twist_mux = Node(
    #     package="twist_mux",
    #     executable="twist_mux",
    #     parameters=[twist_mux_params, {'use_sim_time': True}],
    #     remappings=[('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')]
    # )

    # load_controllers = Node(
    #     package='controller_manager',
    #     executable='spawner.py',
    #     arguments=['--param-file',controllers_yaml],
    #     output='screen'
    # )

    # controller_manager_node = Node(
    #     package='controller_manager',
    #     executable='ros2_control_node',
    #     parameters=[{'robot_description': robot_description},controllers_yaml],
    #     output='screen'
    # )

    # diff_drive_spawner = Node(
    #     package='controller_manager',
    #     executable='spawner.py',
    #     arguments=['diff_drive_controller'],
    #     output='screen'
    # )

    # joint_state_spawner = Node(
    #     package='controller_manager',
    #     executable='spawner.py',
    #     arguments=['joint_state_controller'],
    #     output='screen'
    # )
    # Spawning controllers
    # controller_spawner = Node(
    #     package='controller_manager',
    #     executable='spawner.py',
    #     arguments=['joint_state_controller', 'diff_drive_controller'],
    #     output='screen',
    #     respawn=True
    # )
    # diff_drive_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner.py",
    #     arguments=["diff_cont"],
    # )

    # joint_broad_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner.py",
    #     arguments=["joint_broad"],
    # )   
    

    rviz_node = Node(
        package='rviz2',
         executable='rviz2',
         name='rviz2',
         output='screen',
        arguments=['-d', rvizConfigPath]  # Pass the RViz config file
     )

    # Launch them all!
    return LaunchDescription([
        rsp,
        rplidar_launch,
        #amcl_launch,
        slam_launch,
        rviz_node
        # gazebo,
        # spawn_entity,
        #diff_drive_spawner,
      #  joint_broad_spawner,
        #controller_manager_node,
       # diff_drive_spawner,
        #joint_state_spawner
        # twist_mux,
        
    ])
