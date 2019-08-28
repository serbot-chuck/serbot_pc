#!/usr/bin/env python
# license removed for brevity
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import String
from actionlib_msgs.msg import GoalStatusArray

def pub_return():
    pub = rospy.Publisher('/return', String, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    return_str = "RETURN TO CHARGE"
    pub.publish(return_str)


def movebase_client():

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "laser"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 0.5
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()


def callback(data):
    if data.status_list and data.status_list[0].status == 3:
        pub_return()
        result = movebase_client()
        if result:
            rospy.loginfo("Goal execution done!")


if __name__ == '__main__':
    try:
        rospy.init_node('serbot_return', anonymous=True)
        rospy.Subscriber("move_base/status", GoalStatusArray, callback)
        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
        



 
# def callback(data):
#     rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
# def listener():
#     rospy.init_node('listener', anonymous=True)

#     rospy.Subscriber("move_base/status", String, callback)

#     # spin() simply keeps python from exiting until this node is stopped
#     rospy.spin()

