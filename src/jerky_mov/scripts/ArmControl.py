#!/usr/bin/env python

import rospy

import actionlib
import roslib; roslib.load_manifest('jerky_mov')

from baxter_core_msgs.srv import(
	SolvePositionIK,
	SolvePositionIKRequest
)

from geometry_msgs.msg import(
	Pose
)

from sensor_msgs.msg import(
	JointState
)

from jerky_mov.msg import(
    move_arm_jointsAction,
    move_arm_jointsGoal,
    move_arm_jointsResult,
    move_arm_jointsFeedback
)

from std_msgs.msg import Header
import std_msgs.msg

import copy

from dynamic_reconfigure.server import (
    Server,
)
from jerky_mov.cfg import(
    armConfig,
)
import baxter_interface
import threading
import math
import numpy as np

def convert_baxter_interface_pose(p):
    """
    Converts the pose in baxter_interface to Pose in ROS
    """
    new_pose = Pose()

    new_pose.orientation.w = p['orientation'].w
    new_pose.orientation.x = p['orientation'].x
    new_pose.orientation.y = p['orientation'].y
    new_pose.orientation.z = p['orientation'].z

    new_pose.position.x = p['position'].x
    new_pose.position.y = p['position'].y
    new_pose.position.z = p['position'].z
    return new_pose


class ArmControl:
    """
    The position control system that
    controls the arm based on the the inputs
    """

    #The feedback class for the joint control 
    _joint_fdbk = move_arm_jointsFeedback()
    #Result object for the joint control
    _joint_result = move_arm_jointsResult()
    #Name of the limb that this control system
    #is controlling
    _limb_name = ""
    #A dictionary to store the integral error
    _joint_integral_error = dict()

    def __init__(self, cfg_server, limb_name="left"):
        """
        Constructor
        """
        self._limb_name = limb_name
        #create an instance of the limb
        self._limb = baxter_interface.Limb(self._limb_name)
        #get a list of the joint names
        self._joint_names = self._limb.joint_names()
        #set the target values of each joint to be the current joint angles 
        self._position_targets = self._limb.joint_angles()
        #current velocity target
        self._velocity_targets = self._limb.joint_velocities()
        #current acceleration target
        self._acceleration_targets = self._limb.joint_velocities() ##Didn't really have an acceleration portion in joint state
        #current effort target
        self._effort_targets = self._limb.joint_efforts()

        #get a copy of the dynamic configure server
        self._cfg = cfg_server
        #set the loop rate
        self._loop_rate = rospy.Rate(100);

        #initialize and start the joint action server
        self._as_joints = actionlib.SimpleActionServer(self._limb_name + "ArmJointController", move_arm_jointsAction,
            execute_cb=self.receive_action_joints,auto_start=False)
        self._as_joints.start()
        
        #initialize integral error table 
        for name in self._joint_names:
            self._joint_integral_error[name] = 0


        rospy.loginfo("Arm Control Node online")

    # def _update_feedback(self):
    #     self._fdbk.percent_complete = self._delta_t
    #     #check if any action client is active, if yes, send feedback
    #     if(self._as_pose.is_active()):
    #         self._as_pose.publish_feedback(self._fdbk)


    def receive_action_joints(self, goal):
        """
        Receive and execute the joint targets
        """

        #set the joint_targets to the new position.
        self._position_targets = dict(zip(goal.joints[0].name, goal.joints[0].position))
       # self._velocity_targets = dict(zip(goal.joints[0].name, goal.joints[0].velocity))
        #self._acceleration_targets = dict(zip(goal.joints[0].name, goal.joints[0].effort))
       # self._effort_targets = dict(zip(goal.joints[0].name, goal.joints[0].effort))

        rospy.loginfo("Joint Targets Updated")
        #now we wait for the arm to reach the position
        self._wait_for_target()

        #check again whether the goals is canceled
        #and do the required action.
        if self._as_joints.is_preempt_requested():
            #set the current target to the current target
            self._position_targets = self._limb.joint_angles()
            #confirm the request is preempted
            self._as_joints.set_preempted()
            return

        #set result as complete and sent 
        self._joint_result.complete = True
        self._as_joints.set_succeeded(self._joint_result)


    def _wait_for_target(self, limit=0.2):
        """
        Check and wait for this to reach target
        """

        #get target
        target_vals = np.array(self._position_targets.values())
        #loop until we reach the target or we got request to cancel the target
        while not self._as_joints.is_preempt_requested():
            #get current
            cur_vals = np.array(self._limb.joint_angles().values())

            diff = target_vals - cur_vals
            if np.max(np.abs(diff)) < limit:
                break
            print np.max(np.abs(diff))
            rospy.sleep(0.05)


    def loop(self):
        """
        Main Action Loop
        """
        while not rospy.is_shutdown():
            #do other important stuff here
            #look up whether there is any change in poses, etc...

            #currently, we just update the torques
            self._update_torque()
            #if we have extra time, sleep
            self._loop_rate.sleep()

    def _update_torque(self):
        """
        The torque update loop
        """

        cmd = self._pos_PID_controller()
        #print(cmd)
        self._limb.set_joint_torques(cmd);

    def _pos_PID_controller(self):
        """
        Simple Position Control PID controller
        Gains might be off
        """

        #get the current angles and velocity
        cur_pos = self._limb.joint_angles();
        cur_vel = self._limb.joint_velocities();

        #create the dict for the commanding torques
        cmd = dict();

        #deep copy the target, just in case 
        target_joints = copy.deepcopy(self._position_targets)

        #Run the PID Control System 
        for joint_name in self._joint_names:

            #calculate error
            err = target_joints[joint_name] - cur_pos[joint_name]
            #calculate proportional value

            p = self._cfg.config[joint_name + '_p'] * err;
            i = self._joint_integral_error[joint_name] * self._cfg.config[joint_name + '_i'];
            d = cur_vel[joint_name] * self._cfg.config[joint_name + '_d'] * -1;

            #update integral error
            self._joint_integral_error[joint_name] += (err/100)
            #PID controller
            cmd[joint_name] = p + i + d;

        return cmd

if __name__ == '__main__':
    #initialize node
    rospy.init_node('Baxter_left_arm_controller',anonymous=True)
    #initialize the control class
    ctr = ArmControl()
    #loop forever
    ctr.loop()