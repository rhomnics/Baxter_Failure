#!/usr/bin/env python
#import cv_bridge
#import time
import baxter_interface
import os
import cv2
import rospkg 
import cv_bridge
import rospy
import actionlib
from sensor_msgs.msg import (
    Image,
)
#from baxter_common import EndpointState 

import numpy
import time 

#import rospy

#from baxter_interface import CameraController
#from sensor_msgs.msg import Image

PACKAGE_NAME = "color_detect"
StartDIMX=1024
StartDIMY=600

rospack = rospkg.RosPack()
pack_path = rospack.get_path(PACKAGE_NAME)
base_path = os.path.join(pack_path,'images') 
eye_name='eyes.png'
brow_name="eyebrows.png"
eye_path = os.path.join(base_path, eye_name)
brow_path=os.path.join(base_path, brow_name)

#rospy.init_node('get_camera_image')

#right_camera = CameraController('right_hand_camera')
# boundaries = [
# 	([17, 15, 100], [50, 56, 200]),
# 	([86, 31, 4], [220, 88, 50]),
# 	([25, 146, 190], [62, 174, 250]),
# 	([103, 86, 65], [145, 133, 128])
# ]
# low1=[10, 10, 70]
# up1=[70, 70, 205] #190
# lower1 = np.array(low1, dtype = "uint8")
# upper1 = np.array(up1, dtype = "uint8")
# low2=[10, 10, 125]
# up2=[120, 120, 205] #190
# lower2 = np.array(low2, dtype = "uint8")
# upper2 = np.array(up2, dtype = "uint8")
# head_camera = CameraController('head_camera')

#right_camera.close()
rospy.init_node('EyeMove')
pub=rospy.Publisher('/robot/xdisplay', Image, latch=True, queue_size=1)
done=False
eye_image = cv2.imread(eye_path) 
#cv2.imshow('eye', eye_image)
#cv2.waitKey(0) 
#while not done:
for i in range(0, 20):
    #eye_image = cv2.imread(eye_path) 
    rows, cols, etc = eye_image.shape
    if i%2 == 0:
        M = numpy.float32([[1,0,-50],[0,1,0]])
        dst = cv2.warpAffine(eye_image,M,(cols,rows))
        cv2.rectangle(dst,(974,0),(1024,600),(255,255,255), -1)
    else:
        dst=eye_image
    brow_image = cv2.imread(brow_path) 
    collision_test=cv2.bitwise_or(eye_image, brow_image)
    row_avg = numpy.average(collision_test, axis=0)
    col_avg = numpy.average(row_avg, axis=0)
    print(col_avg)
    complete_pic=cv2.bitwise_and(dst, brow_image)


#cv2.namedWindow('image', cv2.WINDOW_NORMAL)

    #cv2.imwrite('eye_move.png', start_image)

    msg = cv_bridge.CvBridge().cv2_to_imgmsg(complete_pic, encoding="bgr8")
    pub.publish(msg)

    #pub.publish(msg)

    #cv2.imshow('eye', complete_pic)
    #cv2.waitKey(1) 
    time.sleep(1)

#cv2.imshow('eye_shift', dst)
#cv2.imshow('brow', brow_image)
#cv2.imshow('collision', collision_test)
#cv2.imshow('complete', complete_pic)

    
    #print('cant load image')
#cv2.imshow('image', start_image)
cv2.destroyAllWindows()