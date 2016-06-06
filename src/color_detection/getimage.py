import cv_bridge
import time

import rospy

from baxter_interface import CameraController
from sensor_msgs.msg import Image

rospy.init_node('get_camera_image')

left_camera = CameraController('left_hand_camera')
left_camera.resolution = (640, 400)
left_camera.open()

camera_image = None

def get_img(msg):
    global camera_image
    camera_image = msg_to_cv(msg)    

def msg_to_cv(msg):
    return cv_bridge.CvBridge().imgmsg_to_cv(msg, desired_encoding='bgr8')

camera_subscriber = rospy.Subscriber( 'cameras/left_hand_camera/image', Image, get_img)

while camera_image==None:
    pass

print camera_image