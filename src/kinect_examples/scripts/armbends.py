import argparse
import sys
import json
import rospy
import traceback
import baxter_dataflow
import threading
import Queue
from threading import Thread

import baxter_interface
from baxter_interface import CHECK_VERSION

rospy.init_node("kinect_arm_control")
right_arm = baxter_interface.Limb("right")
gripper_right = baxter_interface.Gripper("right", CHECK_VERSION)

if (not gripper_right.calibrated() and
    gripper_right.type() != 'custom'):
    gripper_right.calibrate()

delta=right_arm.joint_angles()
# for key in delta.keys():
#     if key == 'right_s0':
#         delta[key] = 0

print(delta)


# right_arm.move_to_joint_positions(delta, 15.0)