# Autonomous Drone Interceptor System:

Air-to-Air drone interception tracking system built using ROS2 and Gazebo.

## Interception Mission Sequence:

### 1. System Launch & Target Detection
![System Launch](./launch.png)

### 2. Autonomous Tracking Loop
![Autonomous Tracking](./tracking.png)

### 3. Target Neutralization (Kill Zone Trigger)
![Target Interception](./interception.png)

## How to Run
```bash
cd ~/fresh_drone_ws
source install/setup.bash
ros2 launch drone_tracking super_launch.py
