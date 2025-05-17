import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument , TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Define the default path to the parameter YAML file
    
    #default_rviz_config_path = os.path.join(
       # get_package_share_directory("amcl2"), "rviz2", "view_map.rviz"
    #)
    
    default_param_file = os.path.join(
        get_package_share_directory("amcl2"), "params", "map_server.yaml"
    )
    
    default_amcl_param_file = os.path.join(
        get_package_share_directory("amcl2"), "params", "amcl.yaml"
    )


    # Declare a launch argument for the parameter file
    
    #rviz_config_arg = DeclareLaunchArgument(
      #  "rviz_config_file",
       # default_value=default_rviz_config_path,
       # description="Full path to the RViz config file",
   # )
    
    param_file_arg = DeclareLaunchArgument(
        "params_file",
        default_value=default_param_file,
        description="Path to the parameter YAML file"
    )
    
    amcl_param_file_arg = DeclareLaunchArgument(
        "amcl_params_file",
        default_value=default_amcl_param_file,
        description="Path to the AMCL parameter YAML file"
    )


    # Get the parameter file path from launch configuration
    #rviz_config_path = LaunchConfiguration("rviz_config_file")
    param_file_path = LaunchConfiguration("params_file")
    amcl_param_file_path = LaunchConfiguration("amcl_params_file")

    # Node to launch the map server, loading parameters from the YAML file
    
    #rviz_node = Node(
     #   package="rviz2",
      #  executable="rviz2",
       # name="rviz2",
        #output="screen",
        #arguments=["-d", os.path.join(get_package_share_directory("amcl2"), "rviz2", "view_map.rviz")],
#)

    map_server_cmd = Node(
        package="nav2_map_server",
        executable="map_server",
        output="screen",
        parameters=[param_file_path],  # Use the YAML file instead of inline parameters
    )

    #map_server_cmd = TimerAction(
     #   period=2.0,  # Delay map_server by 2 seconds
      #  actions=[
       #     Node(
        #        package="nav2_map_server",
         #       executable="map_server",
          #      output="screen",
           #     parameters=[param_file_path ],
            #)
        #]
    #)
    
    amcl_cmd = TimerAction(
        period=4.0,  # Delay AMCL to ensure map is available first
        actions=[
            Node(
                package="nav2_amcl",
                executable="amcl",
                name ="amcl",
                output="screen",
                parameters=[{'use_sim_time': False},amcl_param_file_path],  # Load AMCL parameters
            )
        ]
    )


    lifecycle_nodes = ["map_server","amcl"]
    use_sim_time = False
    autostart = False

  #  start_lifecycle_manager_cmd = Node(
   #     package="nav2_lifecycle_manager",
    #    executable="lifecycle_manager",
     #   name="lifecycle_manager",
      #  output="screen",
       # emulate_tty=True,
        #parameters=[
         #   {"use_sim_time": use_sim_time},
          #  {"autostart": autostart},
           # {"node_names": lifecycle_nodes},
        #],
    #)

    # Create launch description and add actions
    ld = LaunchDescription()
    
    #ld.add_action(rviz_config_arg)  
    #ld.add_action(rviz_node)
    ld.add_action(param_file_arg) 
    ld.add_action(amcl_param_file_arg) # Add the parameter file argument
    ld.add_action(map_server_cmd)
    ld.add_action(amcl_cmd)
    #ld.add_action(start_lifecycle_manager_cmd)

    return ld
