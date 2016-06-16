#!/usr/bin/env python

# Copyright (c) 2013-2015, Rethink Robotics
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the Rethink Robotics nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Baxter RSDK Joint Trajectory Controller
    Unlike other robots running ROS, this is not a Motor Controller plugin,
    but a regular node using the SDK interface.
"""
import argparse

import rospy

from dynamic_reconfigure.server import Server

from baxter_interface.cfg import (
    PositionJointTrajectoryActionServerConfig,
    VelocityJointTrajectoryActionServerConfig,
    PositionFFJointTrajectoryActionServerConfig,
)
from trajectory import JointTrajectoryActionServer

from trajectory_msgs.msg import (
    JointTrajectoryPoint,
)


def start_server(limb, rate, mode):
    print("Initializing node... ")
    rospy.init_node("rsdk_%s_joint_trajectory_action_server%s" %
                    (mode, "" if limb == 'both' else "_" + limb,))
    print("Initializing joint trajectory action server...")

    dyn_cfg_srv = Server(PositionFFJointTrajectoryActionServerConfig, lambda config, level: config)
    
    #start the two trajectory servers
    j_left = JointTrajectoryActionServer("left", dyn_cfg_srv, rate, mode)
    j_right = JointTrajectoryActionServer('right', dyn_cfg_srv, rate, mode)

    def cleanup():
        j_left.clean_shutdown()
        j_right.clean_shutdown()

    rospy.on_shutdown(cleanup)
    print("Running. Ctrl-c to quit")
    rospy.spin()


def main():
    start_server('both', 100, 'position_w_id')


if __name__ == "__main__":
    main()
