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
from baxter_core_msgs.msg import EndpointState 

import numpy
import time 

#import rospy

#from baxter_interface import CameraController
#from sensor_msgs.msg import Image

PACKAGE_NAME = "color_detect"
StartDIMX=1024
StartDIMY=600
browDIFF=0 

rospack = rospkg.RosPack()
pack_path = rospack.get_path(PACKAGE_NAME)
base_path = os.path.join(pack_path,'scripts') 
eye_name='eyes.png'
brow_name="eyebrows.png"
filter_name="eye_filter.png"
borders_name="eye_circles.png"
eye_path = os.path.join(base_path, eye_name)
brow_path=os.path.join(base_path, brow_name)
filter_path = os.path.join(base_path, filter_name)
borders_path=os.path.join(base_path, borders_name)
filter_image=cv2.imread(filter_path)
borders_image=cv2.imread(borders_path)


def fillBlank(img, diffx, diffy):
    #newimg = img 
    if diffy!=0:
        if diffy>0:
            print("down")
            cv2.rectangle(img, (0,0), (1024, diffy), (255,255,255), -1) 
        else:
            print("up")
            cv2.rectangle(img, (0,600+diffy), (1024, 600), (255,255,255), -1)
    if diffx!=0:
        if diffx>0:
            print("right")
            cv2.rectangle(img, (0,0), (diffx, 600), (255,255,255), -1) 
        else:
            print("left")
            cv2.rectangle(img, (1024+diffx,0), (1024, 600), (255,255,255), -1)
    #return newimg


rospy.init_node('EyeMove')
pub=rospy.Publisher('/robot/xdisplay', Image, latch=True, queue_size=1)
done=False
eye_image = cv2.imread(eye_path) 
brow_image = cv2.imread(brow_path) 
borders_and_brow=cv2.bitwise_and(borders_image, brow_image)

#def collisionDetect

for i in range(0, 20):

    diffx= ((i%4)-1) * 30 * ((i+1)%2)
    diffy= ((i%4)-2) * 15 * (i%2)
  
    print(diffx)
    print(diffy)
    rows, cols, etc = eye_image.shape
    #if i%2 == 0:
    M = numpy.float32([[1,0,diffx],[0,1,diffy]])
    dst = cv2.warpAffine(eye_image,M,(cols,rows))
    fillBlank(dst, diffx, diffy)
    #cv2.rectangle(dst,(974,0),(1024,600),(255,255,255), -1)
    #else:
    #dst=eye_image
    brow_image = cv2.imread(brow_path) 
    collision_test=cv2.bitwise_or(eye_image, brow_image)
    row_min = numpy.amin(collision_test, axis=0)
    col_min= numpy.amin(row_min, axis=0)
    abs_min=numpy.amin(col_min, axis=0)
    #print(abs_min)
    inverse_eyes=cv2.bitwise_not(filter_image)
    just_eyes=cv2.bitwise_or(inverse_eyes, dst)
   
    complete_pic=cv2.bitwise_and(just_eyes, borders_and_brow)






   # msg = cv_bridge.CvBridge().cv2_to_imgmsg(complete_pic, encoding="bgr8")
    #print(msg)
    #pub.publish(msg)
    cv2.imshow('eye', complete_pic)
    cv2.waitKey(1) 
    time.sleep(1)
    if i % 4 == 0:
        inverse_eyes=cv2.bitwise_not(filter_image)
        just_eyes=cv2.bitwise_or(inverse_eyes, eye_image)
        
        complete_pic=cv2.bitwise_and(just_eyes, borders_and_brow)
        #msg = cv_bridge.CvBridge().cv2_to_imgmsg(complete_pic, encoding="bgr8")
        #print(msg)
        #pub.publish(msg)
        cv2.imshow('eye', complete_pic)
        cv2.waitKey(1) 
        time.sleep(1)
cv2.destroyAllWindows()

    


#cv2.destroyAllWindows()


