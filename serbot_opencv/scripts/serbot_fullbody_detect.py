#!/usr/bin/env python
from __future__ import print_function

import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time
import os

def callback(data):
    rate = rospy.Rate(10)
    bridge = CvBridge()
    pub = rospy.Publisher('/fullbodydetect', String, queue_size=2)
    image_pub = rospy.Publisher("/fullbodydetect/image",Image, queue_size=2)
    # allow the camera to warmup  
    time.sleep(0.1)

    model_path = os.path.join(os.path.dirname(__file__), 'haarcascade_fullbody.xml')
    fullbody_cascade = cv2.CascadeClassifier(model_path)

    # capture frames from the camera
    t1 = rospy.get_time()

    try:
      frame = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    fullbody = fullbody_cascade.detectMultiScale(gray, 1.01, 10)
    if (fullbody != None) & (len(fullbody) > 0):
        rospy.loginfo('fullbody detected: %s, started %s took %s' % (str(fullbody), t1, rospy.get_time() - t1))
        pub.publish(str(fullbody))


    for (x,y,w,h) in fullbody:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),3)
    # show the frame
    #cv2.imshow("Frame", image)
    try:
        image_pub.publish(bridge.cv2_to_imgmsg(image, "bgr8"))
    except CvBridgeError as e:
        print(e)

    rate.sleep()
    t1 = rospy.get_time()

def main(args):
  rospy.init_node('serbot_fullbody_detect', anonymous=True)  

  image_sub = rospy.Subscriber("/camera/image",Image, callback)
  

  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
