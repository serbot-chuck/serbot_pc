#!/usr/bin/env python
# license removed for brevity

import sys
import tty
import termios
import rospy
from std_msgs.msg import String

def getKey():
   
    fd = sys.stdin.fileno()
    original_attributes = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, original_attributes)
    return ch


def talker():
    pub = rospy.Publisher("command", String, queue_size=10)
    rospy.init_node('driver', anonymous=True)
#    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = getKey()
        if hello_str == 'q':
           break
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
#        rate.sleep()



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
