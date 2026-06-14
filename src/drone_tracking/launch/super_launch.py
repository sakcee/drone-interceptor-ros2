import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # Package configuration paths
    pkg_drone_tracking = get_package_share_directory('drone_tracking')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # Path to our updated clean empty.world structure
    world_path = os.path.join(pkg_drone_tracking, 'worlds', 'empty.world')

    # 1. Gazebo Server launch description
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world_path}.items()
    )

    # 2. Gazebo Client launcher (Simulation UI GUI)
    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    # 3. Interceptor Tracker Control Logic Node (Zero-drift tracking API)
    interceptor_node = Node(
        package='drone_tracking',
        executable='interceptor_node',
        name='interceptor_node',
        output='screen'
    )

    return LaunchDescription([
        gzserver_cmd,
        gzclient_cmd,
        interceptor_node
    ])