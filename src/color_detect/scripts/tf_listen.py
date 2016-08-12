#!/usr/bin/env python  
import roslib
#roslib.load_manifest('learning_tf')
import rospy
import time
import math
import tf
import geometry_msgs.msg
import sys, traceback


rospy.init_node('console_interface')
t = tf.TransformListener()
rate = rospy.Rate(10)
frames = ""
while len(frames) < 2:
	frames=t.getFrameStrings()
	#print(len(trans))
print(frames)
now = rospy.Time.now()
#ct = t.getLatestCommonTime("reference/base", "reference/head_camera")
#print(type(ct))
#print(ct)
# t.waitForTransform("right_hand", "head_camera",
#                               now, rospy.Duration(100.0));
_time = rospy.Time()
while not t.canTransform("base", "head_camera", _time):
	_time = rospy.Time()
	print("Loop")


#t.waitForTransform("base", "head_camera",
#                              time, rospy.Duration(24 * 60 * 60));

print("success")
print(str(rospy.Time.now() - now))
while not rospy.is_shutdown():
	try:
		(trans, ori)= t.lookupTransform('reference/right_hand', 'reference/head_camera', rospy.Time(0))
		(x,y,z)=trans
		print(x)

	except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
		print("fail")
		continue
	time.sleep(1)


