# Autonomous Humanoid Football Robot (ROS 2 Jazzy)

An end-to-end ROS 2 package for an autonomous humanoid football-playing robot. This project integrates real-time computer vision, kinematic joint control, serial hardware bridging, and 3D visualization in RViz2.

---

## Key Features
* Real-time Ball Detection: Color-space segmentation and contour tracking node using OpenCV to detect the ball from live camera feeds.
* 3D Marker Projection: Converts 2D pixel coordinates into 3D RViz markers for dynamic target visualization relative to the robot base frame.
* Hardware Bridge (serial_bridge.py): Low-latency serial communication between ROS 2 joint trajectory topics and Arduino servo drivers.
* Smooth Velocity Control: Integrated velocity scaling and motion profiling to prevent sudden mechanical jerks upon ball detection.
* Dashboard Visualizer: Custom RViz2 configuration tracking robot pose, joint trajectories, and vision metrics simultaneously.

---

## Package Structure

```text
humanoid_robot/
├── humanoid_robot/
│   ├── __init__.py
│   ├── camera_node.py
│   ├── ball_detector.py
│   ├── ball_tracker_node.py
│   ├── dashboard_visualizer.py
│   └── serial_bridge.py
├── launch/
│   └── display.launch.py
├── urdf/
│   └── humanoid.urdf
├── rviz/
│   └── humanoid_dashboard.rviz
├── resource/
├── test/
├── package.xml
├── setup.py
└── setup.cfg
```
---

## Hardware Requirements
* Custom 3D-Printed Humanoid Chassis
* High-Torque Servo Motors (Calibrated with individual zero-position offsets)
* Buck Converter (DC-DC Step-Down for stable servo power supply)
* Arduino Microcontroller
* USB Webcam
* Host Machine running Ubuntu 24.04 with ROS 2 Jazzy

---

## Prerequisites & Dependencies
* ROS 2 Jazzy Jalisco
* Python 3.12
* OpenCV (python3-opencv)
* PySerial (python3-serial)
* cv_bridge & image_transport
* tf2_ros

---

## Installation & Build

1. Clone the repository into your ROS 2 workspace:
   cd ~/ros2_ws/src
   git clone https://github.com/Ola-Omara/humanoid-robot-ros2.git

2. Install dependencies and build the package:
   cd ~/ros2_ws
   rosdep install --from-paths src --ignore-src -r -y
   colcon build --packages-select humanoid_robot
   source install/setup.bash

---

## Usage

Launch the complete system (Camera, Ball Detector, Serial Bridge, RViz Dashboard, and URDF Model):

ros2 launch humanoid_robot display.launch.py

---

## Real-World Hardware Demonstration

Here are live demonstration videos showing the physical humanoid robot executing gait cycles and forward motion tracking in real-time environments:

* **[Watch Robot Walking Demo - Part 1](https://drive.google.com/file/d/10_vYo4rd44eTG6COKL5IWmJGkHee-hP4/view?usp=sharing)**
* **[Watch Robot Walking Demo - Part 2](https://drive.google.com/file/d/1UI73bFwCQl7cQeI9rwdv0nXbJwFOLM2s/view?usp=sharing)**


## Demonstration & Visuals

### RViz2 Dashboard
![RViz Dashboard](https://drive.google.com/file/d/1WLcOk_dVFRlDDrc3UdurlMTFzOwlYpDF/view?usp=sharing)
