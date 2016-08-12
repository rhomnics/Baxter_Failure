#!/usr/bin/env python

import baxter_interface
import roslib
import os
import cv2
import rospkg 
import cv_bridge
import rospy
import math
import tf
import actionlib
#import statistics
import baxter_interface
import time
from baxter_interface import Limb
from sensor_msgs.msg import (
    Image,
)
from baxter_core_msgs.msg import EndpointState 

import numpy
import time 




class EyeMovement(object):
    def __init__(self, limb="left"):
        self.arm=limb
        self._limb=baxter_interface.Limb(self.arm)
        self._head=baxter_interface.Head()
        self.angle=0.0
        self._head.set_pan(self.angle)
        self._right=baxter_interface.Limb("right")
        self._left=baxter_interface.Limb("left")
        self.PACKAGE_NAME="color_detect"

        #these are the expected dimensions of the image being fed to Baxter
        self.StartDIMX=1024
        self.StartDIMY=600
  
        #this tf listener is used to judge the head's position relative to the body. which changes
        #when the head is rotated
        self.tf_listener=tf.TransformListener()
        frames = ""
        while len(frames) < 2:
            frames=self.tf_listener.getFrameStrings()


        #head's relative position to the body
        self.headX=.187
        self.headY=.018
        self.headZ=.750

        #ratio ranges between 0 and 1 and indicates what percentage of the view is held be the left hand
        self.limbRatio=.5
        #vector perpendicular to robot's screen for calculating distance of hand from face
        self.depthVector=[1,0]

        #vector paralell to robot's face vector starts out parallel to y axis

        self.screenVector=[0,-1]

        #for far is the screen vector is from 0,0, is initially -.018
        self.offset=-.187


        #this sectioon is used to find the head's initial position in relation to the body more
        #specifically the head camera
        self.now = rospy.Time.now()
        # self.tf_listener.waitForTransform("base", "head_camera",
        #                       self.now, rospy.Duration(500.0));
        _time = rospy.Time()
        while not self.tf_listener.canTransform("base", "head_camera", _time):
            _time = rospy.Time()
        print("Loop")

        print("success")
        print(str(rospy.Time.now() - self.now))
        try:
           (trans, ori)= self.tf_listener.lookupTransform('reference/base', 'reference/head_camera', rospy.Time(0))
           (x,y,z)=trans
           self.headX=x
           self.headY=y
           self.headZ=z    

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
           print("fail")
           #continue

        ##NOTE##
        # self.periph is how far the robot's periphial vision extends given the distance of the hand from
        #it's face 
        self.periph=0 


        #this is section loads the images used to create the moving eye effect
        #eye_image contains only the pupils, the filter_image is used to create the layered effect,
        #that makes the pupils appear to be behind the borders of the eyes. The final image, as it's name
        #suggests contains the eyes borders and brow, which is layered on top of the filtered image after
        #each shift
        self.rospack = rospkg.RosPack()
        self.pack_path = self.rospack.get_path(self.PACKAGE_NAME)
        self.base_path = os.path.join(self.pack_path,'images') 
        self.eye_name='eyes.png'
        self.brow_name="eyebrows.png"
        self.filter_name="eye_filter.png"
        self.borders_name="eye_circles.png"
        self.eye_path = os.path.join(self.base_path, self.eye_name)
        self.brow_path=os.path.join(self.base_path, self.brow_name)
        self.filter_path = os.path.join(self.base_path, self.filter_name)
        self.borders_path=os.path.join(self.base_path, self.borders_name)
        self.filter_image=cv2.imread(self.filter_path)
        self.borders_image=cv2.imread(self.borders_path)
        self.eye_image = cv2.imread(self.eye_path) 
        #self.brow_image = cv2.imread(self.brow_path) 
        self.borders_and_brow=self.borders_image#cv2.bitwise_and(self.borders_image, self.brow_image)

        
        self._rs = baxter_interface.RobotEnable()
        self._init_state = self._rs.state().enabled

        #this just gets the dimentionality of the eye_image (note this should be 1024x600)
        self.rows, self.cols, self.o = self.eye_image.shape

        #the publisher that actually sends the robot to Baxter's screen
        self.pub=rospy.Publisher('/robot/xdisplay', Image, latch=True, queue_size=1)
        self.done=False

        #keeps track of how long baxter has been immobile
        self.stillCounter=0

    def getNewHeadCoords(self):
        try:
            (trans, ori)= self.tf_listener.lookupTransform('reference/base', 'reference/head_camera', rospy.Time(0))
            (x,y,z)=trans
            self.headX=x
            self.headY=y
            self.headZ=z    

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print("fail")
    def calculatePeriph(self, x, y):

        xVal=self.screenVector[1]*x
        yVal=self.screenVector[0]*y*(-1)

        #dist=math.fabs(self.headX-x)
        dist=math.fabs(xVal+yVal+self.offset)
        #print(dist)
        self.periph=(dist*math.tan(0.261799)) + .001
    def setVectors(self):
        self.depthVector=[math.cos(self.angle), math.sin(self.angle)]
        self.screenVector=[math.sin(self.angle), -math.cos(self.angle)]
        self.offset=0-((self.screenVector[1]*self.headX) - (self.screenVector[0]*self.headY))


    def getCombinedCoord(self):
        posR=self.getEnpoint("right")
        posL=self.getEnpoint("left")
        

    def project(self, r):
        nominator=(r[0]*self.screenVector[0])+(r[1]*self.screenVector[1])
        denominator=1
        if denominator==0:
            return 0
        else:
            return (nominator/denominator)
    def calculateHShift(self, x, y):
        dist=0
        sign=1
        r=[self.headX-x, self.headY-y]
        dist=self.project(r)
        #print(self.headX)
        #if (self.headY-y) > 0:
        if dist < 0:
            sign=-1
        #if math.fabs(self.headY-y) > self.periph:
        if math.fabs(dist) > self.periph:
            dist=self.periph*sign
            #baxter_interface.Head().pan(0.261799)
            self.angle=self.angle+(0.261799*sign)
            if self.angle < -1.4:
                self.angle=-1.4
            if self.angle > 1.4:
                self.angle=1.4
            self._head.set_pan(self.angle)
            while self._head.panning():
               pass
            self.getNewHeadCoords()
            self.angle=self._head.pan()
           # print(self.angle)
            self.setVectors()

            #print("head coords changed")

        else:
            #dist=self.headY-y
            dist=dist

        ratio = math.fabs(dist/self.periph)

        hShift=int(30*ratio)*sign
        return hShift
    def calculateVShift(self, z):
        dist=0
        sign=1
        if (self.headZ-z) < 0:
            sign=-1
        if math.fabs(self.headZ-z) > self.periph:

            dist=self.periph*sign
        else:
            dist=self.headZ-z

        ratio = math.fabs(dist/self.periph)

        vShift=int(55*ratio)*sign
        return vShift




    def fillBlank(self, img, diffx, diffy):
      
        if diffy!=0:
            if diffy>0:
                #print("down")
                cv2.rectangle(img, (0,0), (1024, diffy), (255,255,255), -1) 
            else: 
               # print("up")
                cv2.rectangle(img, (0,600+diffy), (1024, 600), (255,255,255), -1)
        if diffx!=0:
            if diffx>0:
                #print("right")
                cv2.rectangle(img, (0,0), (diffx, 600), (255,255,255), -1) 
            else:
               # print("left")
                cv2.rectangle(img, (1024+diffx,0), (1024, 600), (255,255,255), -1)

    def generateImage(self, diffx, diffy):
        M = numpy.float32([[1,0,diffx],[0,1,diffy]])
        dst = cv2.warpAffine(self.eye_image,M,(self.cols,self.rows))
        self.fillBlank(dst, diffx, diffy)
        inverse_eyes=cv2.bitwise_not(self.filter_image)
        just_eyes=cv2.bitwise_or(inverse_eyes, dst)
        #switch here 
        complete_pic=cv2.bitwise_and(just_eyes, self.borders_and_brow)
        return complete_pic 

    def sendImage(self, img):
        msg = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
    #print(msg)
        self.pub.publish(msg)

    def clean_shutdown(self):
        print("\nExiting example...")
        if not self._init_state:
            print("Disabling robot...")
    
        return True
    def getEndpoint(self):
        posl=self._left.endpoint_pose()
        posr=self._right.endpoint_pose()
        (xl,yl,zl)=posl['position']
        (xr,yr,zr)=posr['position']
        x=(xl*self.limbRatio)+(xr * (1-self.limbRatio))
        y=(yl*self.limbRatio)+(yr * (1-self.limbRatio))
        z=(zl*self.limbRatio)+(zr * (1-self.limbRatio))
        pos=(x,y,z)
        #print("got xyz")
        #print(pos['position'])
        return (x,y,z)

    def getLimbEndpoint(self, limb):
        pos=self._limb.endpoint_pose()
        return pos['position']

    #def flickEyes

    def calculateMovementRatio(self, prevpos, newpos):
        right_delta=math.sqrt(math.fsum([math.pow((prevpos[1][0]-newpos[1][0]), 2), 
            math.pow((prevpos[1][1]-newpos[1][1]), 2), 
            math.pow((prevpos[1][2]-newpos[1][2]), 2)]))
        left_delta=math.sqrt(math.fsum([math.pow((prevpos[0][0]-newpos[0][0]), 2), 
            math.pow((prevpos[0][1]-newpos[0][1]), 2), 
            math.pow((prevpos[0][2]-newpos[0][2]), 2)]))
        right_veloctiy=self._right.joint_velocities()
        left_velocity=self._left.joint_velocities()
        sumr=0
        suml=0
        for joint, val in right_veloctiy.items():
            #print(val)
            sumr+=math.fabs(val)
        for joint, val in left_velocity.items():
            suml+=math.fabs(val)

        #total_change=left_delta + right_delta
        #print(suml)
        if suml < .1 or sumr < .1:
            self.stillCounter+=1
            if self.stillCounter>=8:
                self.flickEyes()
                self.stillCounter= 0
        else:
            self.stillCounter= 0
        #print(sumr)
        if math.fabs(suml-sumr)<.1:
            self.limbRatio=self.limbRatio #+(.5*.1)
           # print("cheers")
        elif sumr>suml:
            self.limbRatio= max(self.limbRatio-.5, 0.0)
           # print("nomp")
           # print("i'm moving")

        else:
            self.limbRatio= min(self.limbRatio+.5, 1.0)
           # print("nomp")
            #print('fuuuuuu')
        #print(self.limbRatio)
    def flickEyes(self):
        print("flick")
        right_veloctiy=self._right.joint_velocities()
        left_velocity=self._left.joint_velocities()
        sumr=0
        suml=0
        for joint, val in right_veloctiy.items():
            #print(val)
            sumr+=math.fabs(val)
        for joint, val in left_velocity.items():
            suml+=math.fabs(val)
        switch=0
        sign=1
        while sumr<.15 and suml<.15 and not rospy.is_shutdown():
            if switch>200:
                sign=-1*sign
                switch=0

            img=self.generateImage(60*sign, 25)
            self.sendImage(img)
            switch+=1
            right_veloctiy=self._right.joint_velocities()
            left_velocity=self._left.joint_velocities()
            sumr=0
            suml=0
            for joint, val in right_veloctiy.items():
                #print(val)
                sumr+=math.fabs(val)
            for joint, val in left_velocity.items():
                suml+=math.fabs(val)
            #print("left:"+str(suml))
            #print("right:"+str(sumr))




def main():
    print("Initializing node... ")
    rospy.init_node('EyeMove')

    moveEye=EyeMovement("left")

    rospy.on_shutdown(moveEye.clean_shutdown)
    print("Starting Eye Movements")
    prevpos=[moveEye.getLimbEndpoint('left'), moveEye.getLimbEndpoint('right')]
    lastime=time.time()
    while not rospy.is_shutdown():
        if time.time()-lastime > .5:

            newpos=[moveEye.getLimbEndpoint("left"), moveEye.getLimbEndpoint('right')]
            moveEye.calculateMovementRatio(prevpos, newpos)
            prevpos=newpos
            lastime=time.time()
        pos=moveEye.getEndpoint()
  
        #print(pos)
        (x,y,z)=pos

        
        


        #print("got xyz")
        moveEye.calculatePeriph(x,y)

        xpos=moveEye.calculateHShift(x, y)
        ypos=moveEye.calculateVShift(z)
        comp=moveEye.generateImage(xpos, ypos)
        moveEye.sendImage(comp)
    
if __name__ == '__main__':
    main()





#cv2.destroyAllWindows()

    


#cv2.destroyAllWindows()


