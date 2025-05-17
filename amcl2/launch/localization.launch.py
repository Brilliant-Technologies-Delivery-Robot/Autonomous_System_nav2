import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration
from nav2_common.launch import RewrittenYaml




def generate_launch_description():
    bringup_dir = get_package_share_directory("amcl2")

    # Declare launch arguments
    namespace = LaunchConfiguration("namespace")
    use_sim_time = LaunchConfiguration("use_sim_time")
    autostart = LaunchConfiguration("autostart")
    params_file = LaunchConfiguration("params_file")

    # Map file path
    map_file_path = os.path.join(
        get_package_share_directory("amcl2"), "maps", "turtlebot3_world.yaml"
    )

    # Configure remappings
    remappings = [("/tf", "tf"), ("/tf_static", "tf_static")]

    # Parameter substitutions
    param_substitutions = {"use_sim_time": use_sim_time, "yaml_filename": map_file_path}

    configured_params = RewrittenYaml(
        source_file=params_file,
        root_key=namespace,
        param_rewrites=param_substitutions,
        convert_types=True,
    )

    # Nodes
    map_server_cmd = Node(
        package="nav2_map_server",
        executable="map_server",
        name="map_server",
        output="screen",
        parameters=[{"yaml_filename": map_file_path}],
    )

    amcl_cmd = Node(
        package="nav2_amcl",
        executable="amcl",
        name="amcl",
        output="screen",
        namespace=namespace,
        parameters=[configured_params],
        remappings=remappings,
    )

    lifecycle_nodes = ["map_server", "amcl"]

    start_lifecycle_manager_cmd = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager",
        output="screen",
        parameters=[
            {"use_sim_time": use_sim_time},
            {"autostart": autostart},
            {"node_names": lifecycle_nodes},
        ],
    )

    # Return launch description with properly added actions
    return LaunchDescription(
        [
            SetEnvironmentVariable("RCUTILS_LOGGING_BUFFERED_STREAM", "1"),
            DeclareLaunchArgument(
                "namespace", default_value="", description="Top-level namespace"
            ),
            DeclareLaunchArgument(
                "map",
                default_value=map_file_path,
                description="Full path to map yaml file to load",
            ),
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use simulation (Gazebo) clock if true",
            ),
            DeclareLaunchArgument(
                "autostart",
                default_value="true",
                description="Automatically startup the nav2 stack",
            ),
            DeclareLaunchArgument(
                "params_file",
                default_value=os.path.join(bringup_dir, "params", "amcl.yaml"),
                description="Full path to the ROS2 parameters file to use",
            ),
            # Add node actions
            map_server_cmd,
            amcl_cmd,
            start_lifecycle_manager_cmd,
     
        ]
    )
