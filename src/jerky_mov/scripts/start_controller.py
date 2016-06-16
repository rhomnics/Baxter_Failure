#!/usr/bin/env python

import rospy

from dynamic_reconfigure.server import (
    Server,
)
from jerky_mov.cfg import(
    armConfig,
)

from ArmControl import ArmControl

def main():

    rospy.init_node("arm_controller")

    cfg_server = Server(armConfig, lambda config, level: config)

    #start two arm control for the robot
    right_arm = ArmControl(cfg_server, "right")
    left_arm = ArmControl(cfg_server, "left")

    _loop_rate = rospy.Rate(100)

    while not rospy.is_shutdown():
        #do other important stuff here
        #look up whether there is any change in poses, etc...

        #currently, we just update the torques
        right_arm._update_torque()
        left_arm._update_torque()
        #if we have extra time, sleep
        _loop_rate.sleep()


if __name__ == '__main__':
    main()