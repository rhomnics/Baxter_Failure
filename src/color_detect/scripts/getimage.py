#!/usr/bin/env python
import cv_bridge
import time
import cv2
import numpy as np

import rospy

from baxter_interface import CameraController
from sensor_msgs.msg import Image




rospy.init_node('get_camera_image')

#right_camera = CameraController('right_hand_camera')
boundaries = [
	([17, 15, 100], [50, 56, 200]),
	([86, 31, 4], [220, 88, 50]),
	([25, 146, 190], [62, 174, 250]),
	([103, 86, 65], [145, 133, 128])
]
low1=[10, 10, 70]
up1=[70, 70, 205] #190
lower1 = np.array(low1, dtype = "uint8")
upper1 = np.array(up1, dtype = "uint8")
low2=[10, 10, 125]
up2=[120, 120, 205] #190
lower2 = np.array(low2, dtype = "uint8")
upper2 = np.array(up2, dtype = "uint8")
head_camera = CameraController('head_camera')
#right_camera.close()
print("closed right")
left_camera = CameraController('left_hand_camera')
head_camera.open()
left_camera.resolution = (640, 400)
left_camera.open()
print("camera open")

camera_image = None
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
def get_img(msg):
    global camera_image
    camera_image = msg_to_cv(msg)
    mask = cv2.inRange(camera_image, lower1, upper1)
    mask2=cv2.inRange(camera_image, lower2, upper2)
    mask3=cv2.bitwise_or(mask, mask2)
    blur =cv2.GaussianBlur(camera_image,(5,5),0)
    output = cv2.bitwise_and(camera_image, camera_image, mask = mask3)
    #mask = cv2.inRange(camera_image, lower, upper)
	#output = cv2.bitwise_and(camera_image, camera_image, mask = mask)
    median = cv2.medianBlur(camera_image,5)
    cv2.imshow('image', camera_image)
    cv2.waitKey(1) 
	#cv2.namedWindow('image', cv2.WINDOW_NORMAL)
	#cv2.imshow('image', camera_image)
	#cv2.waitKey(0)   

def msg_to_cv(msg):
	return cv_bridge.CvBridge().imgmsg_to_cv2(msg, desired_encoding='bgr8')

camera_subscriber = rospy.Subscriber( 'cameras/left_hand_camera/image', Image, get_img)
rospy.spin()
while camera_image==None:
	pass


#rospy.spin()
#cv2.destroyAllWindows()
#print camera_image