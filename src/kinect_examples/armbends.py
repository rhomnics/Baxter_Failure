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

right_arm = baxter_interface.Limb("right")
gripper_right = baxter_interface.Gripper("right", CHECK_VERSION)