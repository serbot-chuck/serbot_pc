################################################################################
# Set minimum required version of cmake, project name and compile options
################################################################################
cmake_minimum_required(VERSION 2.8.3)
project(serbot_example)

################################################################################
# Find catkin packages and libraries for catkin and system dependencies
################################################################################
find_package(catkin REQUIRED COMPONENTS
  rospy
  actionlib
  interactive_markers
  std_msgs
  sensor_msgs
  geometry_msgs
  nav_msgs
  visualization_msgs
  actionlib_msgs
  serbot_msgs
  message_generation
)

################################################################################
# Setup for python modules and scripts
################################################################################
catkin_python_setup()

################################################################################
# Declare ROS messages, services and actions
################################################################################
add_action_files(
  FILES
  serbot.action
)

generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
  actionlib_msgs
)

################################################################################
# Declare ROS dynamic reconfigure parameters
################################################################################

################################################################################
# Declare catkin specific configuration to be passed to dependent projects
################################################################################
catkin_package(
  CATKIN_DEPENDS
    rospy
    actionlib
    interactive_markers
    std_msgs
    sensor_msgs
    geometry_msgs
    nav_msgs
    visualization_msgs
    actionlib_msgs
    serbot_msgs
    message_runtime
)

################################################################################
# Build
################################################################################
include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

################################################################################
# Install
################################################################################
catkin_install_python(PROGRAMS 
  nodes/serbot_obstacle
  nodes/serbot_client
  nodes/serbot_server
  nodes/serbot_pointop_key
  nodes/serbot_bumper 
  nodes/serbot_cliff
  nodes/serbot_sonar
  nodes/serbot_illumination
  nodes/serbot_marker_server
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch rviz
	DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

################################################################################
# Test
################################################################################
