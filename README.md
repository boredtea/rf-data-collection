# RB5 Utilities

A collection of ROS 2 Foxy utility nodes for the RB5 platform, including IMU publishing, teleoperation, video recording, map saving, and camera management tools.

---

## 🛠️ Setup Instructions

First, clone and build the repository:

```
git clone https://github.com/boredtea/rf-data-collection
cd rf-data-collection
```

Make sure to source ROS 2 Foxy every time you open a new terminal and run the commands below:

```bash
source /opt/ros/foxy/setup.bash
colcon build
source install/setup.bash
```

## Available Utilities
This repository contains multiple utility nodes. See below for usage instructions.

### Camera and Mapping Tools
**Launch Camera Driver**
```
ros2 launch utils camera_main_launch.py
```
- If `GSCAM_CONFIG` is already set, unset it before running:
    `unset GSCAM_CONFIG`


**View Camera Feed**
```
ros2 run utils camera_viewer
```

**Record Video from Camera**
```
ros2 run utils video_recorder
```

**Save Map**
```
ros2 run utils map_saver
```

### IMU Node
Publishes IMU data from the RB5.
```
ros2 run imu-ros2node imu-ros2node
```

### Teleoperation with Keyboard
Use your keyboard to send velocity commands, and receive them on a subscriber node.

**Terminal 1: Teleop Sender**
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
**Terminal 2: Teleop Subscriber**
```
ros2 run teleop_subscriber cmd_vel_subscriber
```

## Notes
- Maintained by [Soumi Chakraborty](linkedin.com/in/soumi-chakraborty-a5365b1a7/).
- Some of these utilities rely on other ROS topics (e.g., `/image_raw`, `/cmd_vel`). Please check the source code for each utility to understand its dependencies and ensure the required publishers are running.
- Refer to [https://github.com/boredtea/orb_slam_docker](https://github.com/boredtea/orb_slam_docker) for a containerized version of ORB SLAM to build a complete map.