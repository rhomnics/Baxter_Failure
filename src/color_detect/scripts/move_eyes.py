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
        ##NOTE##
        #self.angle is the current angular position of the head
        #the set_pan command ensures the head starts looking forward
        self.angle=0.0
        self._head.set_pan(self.angle)
        self._right=baxter_interface.Limb("right")
        self._left=baxter_interface.Limb("left")
        self.PACKAGE_NAME="color_detect"

        ##NOTE##
        #these are the expected dimensions of the image being fed to Baxter
        self.StartDIMX=1024
        self.StartDIMY=600
        
        ##NOTE##
        #this tf listener is used to judge the head's position relative to the body. which changes
        #when the head is rotated
        self.tf_listener=tf.TransformListener()
        frames = ""
        while len(frames) < 2:
            frames=self.tf_listener.getFrameStrings()

        ##NOTE##
        #head's relative position to the body
        self.headX=.187
        self.headY=.018
        self.headZ=.750

        ##NOTE##
        #ratio ranges between 0 and 1 and indicates what percentage of the view is held be the left hand
        self.limbRatio=.5

        ##NOTE##
        #vector perpendicular to robot's screen for calculating distance of hand from face
        self.depthVector=[1,0]

        ##NOTE##
        #vector paralell to robot's face vector starts out parallel to y axis
        self.screenVector=[0,-1]

        ##NOTE##
        #for far is the screen vector is from 0,0, is initially -.018
        self.offset=-.187

        ##NOTE##
        #this sectioon is used to find the head's initial position in relation to the body more
        #specifically the head camera
        self.now = rospy.Time.now()
        self.tf_listener.waitForTransform("base", "head_camera",
                              self.now, rospy.Duration(100.0));

        try:
           (trans, ori)= self.tf_listener.lookupTransform('reference/base', 'reference/head_camera', rospy.Time(0))
           (x,y,z)=trans
           self.headX=x
           self.headY=y
           self.headZ=z    

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
           print("fail")


        ##NOTE##
        # self.periph is how far the robot's periphial vision extends given the distance of the hand from
        #it's face 
        self.periph=0 

        ##NOTE##
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
        self.borders_and_brow=self.borders_image

        
        self._rs = baxter_interface.RobotEnable()
        self._init_state = self._rs.state().enabled

        ##NOTE##
        #this just gets the dimentionality of the eye_image (note this should be 1024x600)
        self.rows, self.cols, self.o = self.eye_image.shape

        ##NOTE##
        #the publisher that actually sends the robot to Baxter's screen
        self.pub=rospy.Publisher('/robot/xdisplay', Image, latch=True, queue_size=1)
        self.done=False

        ##NOTE##
        #keeps track of how long baxter has been immobile
        self.stillCounter=0

    def getNewHeadCoords(self):
        #this function essentially does the same thing that was done when initializing
        #the node.
        #it gets Baxter's head coordinates using a tf listener if Baxter moves its head
        try:
            (trans, ori)= self.tf_listener.lookupTransform('reference/base', 'reference/head_camera', rospy.Time(0))
            (x,y,z)=trans
            self.headX=x
            self.headY=y
            self.headZ=z    

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print("fail")

    def calculatePeriph(self, x, y):
        #this uses the vector parallel to the robot's screen 
        #to calculate the point of focus's current distance from the screen
        #along the vector parallel to the screen's normal vector
        #the formula used can be found here 
        #http://mathworld.wolfram.com/Point-LineDistance2-Dimensional.html
        xVal=self.screenVector[1]*x
        yVal=self.screenVector[0]*y*(-1)


        dist=math.fabs(xVal+yVal+self.offset)

        self.periph=(dist*math.tan(0.261799)) + .001

    def setVectors(self):
        #this function sets the new directional vectors of the screen based on the pan angle
        self.depthVector=[math.cos(self.angle), math.sin(self.angle)]
        self.screenVector=[math.sin(self.angle), -math.cos(self.angle)]
        self.offset=0-((self.screenVector[1]*self.headX) - (self.screenVector[0]*self.headY))


    def project(self, r):

        #this returns the projection of the vector from the point to the screen 
        #(which has already been projected onto the xy plane) onto the vector parallel to
        #the screen's width
        projection=(r[0]*self.screenVector[0])+(r[1]*self.screenVector[1])

        return projection

    def calculateHShift(self, x, y):
        #this calculate the horizontal distance from the center
        #of the robot's gaze proportional to the robot's periphial vision
        #and translate that to a shift between 0 and 30 pixels
        #also rotates the robot's head if its eyes are above 30 degree shift
        dist=0
        sign=1
        r=[self.headX-x, self.headY-y]
        dist=self.project(r)
        if dist < 0:
            sign=-1
        if math.fabs(dist) > self.periph:
            dist=self.periph*sign
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
            self.setVectors()



        else:
            #dist=self.headY-y
            dist=dist

        ratio = math.fabs(dist/self.periph)

        hShift=int(30*ratio)*sign
        return hShift
    def calculateVShift(self, z):
        #see calculateHShift, this simply does it in the verticle direction
        #no head movement since the head can only nod.
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
        #this is used to fill in the empty gaps cause by translating the
        #eye_image in order to shift the pupils
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
        #this sfits the eyes according to the calulated distance,
        #filters them so that the pupils don't show outside the border,
        #and then merges the filtered pupil image with the eye borders and the eyebrows
        M = numpy.float32([[1,0,diffx],[0,1,diffy]])
        dst = cv2.warpAffine(self.eye_image,M,(self.cols,self.rows))
        self.fillBlank(dst, diffx, diffy)
        inverse_eyes=cv2.bitwise_not(self.filter_image)
        just_eyes=cv2.bitwise_or(inverse_eyes, dst)
        complete_pic=cv2.bitwise_and(just_eyes, self.borders_and_brow)
        return complete_pic 

    def sendImage(self, img):
        msg = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
        self.pub.publish(msg)

    def clean_shutdown(self):
        print("\nExiting example...")
        if not self._init_state:
            print("Disabling robot...")
    
        return True
    def getEndpoint(self):
        #this assigns a point of focus based on which limb is the most active. If neither limp is active
        #it looks somewhere in the center of the two limbs
        posl=self._left.endpoint_pose()
        posr=self._right.endpoint_pose()
        (xl,yl,zl)=posl['position']
        (xr,yr,zr)=posr['position']
        x=(xl*self.limbRatio)+(xr * (1-self.limbRatio))
        y=(yl*self.limbRatio)+(yr * (1-self.limbRatio))
        z=(zl*self.limbRatio)+(zr * (1-self.limbRatio))
        pos=(x,y,z)
        return (x,y,z)

    def getLimbEndpoint(self, limb):
        pos=self._limb.endpoint_pose()
        return pos['position']


    def calculateMovementRatio(self, prevpos, newpos):
        #this determines which limb the robot should pay attention to based on its movement
        right_veloctiy=self._right.joint_velocities()
        left_velocity=self._left.joint_velocities()
        sumr=0
        suml=0
        for joint, val in right_veloctiy.items():
            #print(val)
            sumr+=math.fabs(val)
        for joint, val in left_velocity.items():
            suml+=math.fabs(val)

        if suml < .1 or sumr < .1:
            self.stillCounter+=1
            if self.stillCounter>=8:
                self.flickEyes()
                self.stillCounter= 0
        else:
            self.stillCounter= 0

        if math.fabs(suml-sumr)<.1:
            self.limbRatio=self.limbRatio
        elif sumr>suml:
            self.limbRatio= max(self.limbRatio-.5, 0.0)


        else:
            self.limbRatio= min(self.limbRatio+.5, 1.0)

    def flickEyes(self):
        #this flicks the eyes back and forth if the robots is imobile too long
        print("flick")
        right_veloctiy=self._right.joint_velocities()
        left_velocity=self._left.joint_velocities()
        sumr=0
        suml=0
        for joint, val in right_veloctiy.items():

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

                sumr+=math.fabs(val)
            for joint, val in left_velocity.items():
                suml+=math.fabs(val)





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


