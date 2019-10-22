#include <ros/ros.h>
#include <tf/transform_broadcaster.h>

int main(int argc, char** argv){
  ros::init(argc, argv, "serbot_tf_publisher");
  ros::NodeHandle nh;

  ros::Rate r(100);

  tf::TransformBroadcaster footprint_to_base_broadcaster;
  tf::TransformBroadcaster base_to_scan_broadcaster;

  while(nh.ok()){
    footprint_to_base_broadcaster.sendTransform(
      tf::StampedTransform(
        tf::Transform(tf::Quaternion(0, 0, 0, 1), tf::Vector3(0.0, 0.0, 0.0)),
        ros::Time::now(), "base_footprint" ,"base_link"));
    base_to_scan_broadcaster.sendTransform(
      tf::StampedTransform(
        tf::Transform(tf::Quaternion(0, 0, 0, 1), tf::Vector3(0.0, 0.0, 0.0)),
        ros::Time::now(),"base_link", "base_scan"));
//    base_to_laser_broadcaster.sendTransform( 
//      tf::StampedTransform(
//        tf::Transform(tf::Quaternion(0, 0, 0, 1), tf::Vector3(0, 0, 0)),
//        ros::Time::now(),"base_laser", "camera_link"));
    r.sleep();
  }
}
