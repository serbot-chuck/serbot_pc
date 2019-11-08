#!/usr/bin/env python
# license removed for brevity
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import String
from actionlib_msgs.msg import GoalStatusArray
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

msg = """
Control Your Serbot!
---------------------------
Moving toward(select 0,1,2,3):

space key, s : force stop

CTRL-C to quit
"""

e = """
Communications Failed
"""

def getKey():
    if os.name == 'nt':
      return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def pub_stop():
    pub = rospy.Publisher('/fullbodydetect/stop', String, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    stop_str = "STOP MOTOR"
    pub.publish(stop_str)


def movebase_client():

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"

    try:
        print msg
        while(1):
            key = getKey()
            if key == '0' :
                print key               
                goal.target_pose.header.stamp = rospy.Time.now()
                goal.target_pose.pose.position.x = 2.3
                goal.target_pose.pose.position.y = 0.05
                goal.target_pose.pose.position.z = 0.0
                goal.target_pose.pose.orientation.w = 1.0
                client.send_goal(goal)
            elif key == '1' :
                print key
                goal.target_pose.header.stamp = rospy.Time.now()
                goal.target_pose.pose.position.x = 1.4
                goal.target_pose.pose.position.y = -0.4
                goal.target_pose.pose.position.z = 0.0
                goal.target_pose.pose.orientation.w = 1.0
                client.send_goal(goal)
            elif key == '2' :
                print key
                goal.target_pose.header.stamp = rospy.Time.now()
                goal.target_pose.pose.position.x = 1.5
                goal.target_pose.pose.position.y = 0.5
                goal.target_pose.pose.position.z = 0.0
                goal.target_pose.pose.orientation.w = 1.0
                client.send_goal(goal)
            elif key == '3' :
                print key
                goal.target_pose.header.stamp = rospy.Time.now()
                goal.target_pose.pose.position.x = 0.0
                goal.target_pose.pose.position.y = 0.0
                goal.target_pose.pose.position.z = 0.0
                goal.target_pose.pose.orientation.w = 1.0
                client.send_goal(goal)
            elif key == ' ' or key == 's' :
                print key
                pub_stop()
            else:
                if (key == '\x03'):
                    break

    except:
        print e

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

########################eunyeong####play_reached_sound#####################################
#global pub_sound = rospy.Publisher('/play_sound_file/reached', String, queue_size=10)
#global tts_param = rospy.get_param('tts_file', '/home/chuck/Downloads/reached.mp3')
## have to write param in launch file ####

def move_default():
    #pub_sound.publish(tts_param)
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 0.0
    goal.target_pose.pose.position.y = 0.0
    goal.target_pose.pose.position.z = 0.0
    goal.target_pose.pose.orientation.w = 1.0
    client.send_goal(goal)
    rospy.loginfo("serbot is moving back")


if __name__ == '__main__':
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    try:
        rospy.init_node('serbot_return', anonymous=True)
#        rospy.Subscriber("move_base/status", GoalStatusArray, callback)
#        rospy.spin()
#        pub_return()
        result = movebase_client()
        rospy.Subscriber("/return", String, move_default)
        if result:
            rospy.loginfo("Goal execution done!")
            pubReached = rospy.Publisher('/reached', String, queue_size=10)
            reached_str = "Goal Reached"
            pubReached.publish(reached_str)

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
        



 
# def callback(data):
#     rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
# def listener():
#     rospy.init_node('listener', anonymous=True)

#     rospy.Subscriber("move_base/status", String, callback)

#     # spin() simply keeps python from exiting until this node is stopped
#     rospy.spin()

