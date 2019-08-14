#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

import rospy
from std_msgs.msg import String

pub = None
hello = None

def facedetect_callback(data):
    rospy.loginfo(rospy.get_caller_id() + ': face detect received: %s', data.data)
    #pub.publish(hello)


def listener():
    global pub
    global hello

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('facedetect_listener_node', anonymous=True)
    pub = rospy.Publisher('/play_sound_file', String, queue_size=10)
    #hello = rospy.get_param('hello', '/home/chuck/Downloads/tts.mp3')

    rospy.Subscriber('/facedetect', String, facedetect_callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
