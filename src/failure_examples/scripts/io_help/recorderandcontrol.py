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

import rospy

import baxter_interface
import baxter_external_devices

from baxter_interface import CHECK_VERSION

class JointRecorder(object):
    def __init__(self, filename, rate):
        """
        Records joint data to a file at a specified rate.
        """
        self._filename = filename
        self._raw_rate = rate
        self._rate = rospy.Rate(rate)
        self._start_time = rospy.get_time()
        self._time_shift=0
        self._done = False
        self._pause= False
        #self._navigator_io = baxter_interface.Navigator("right")

        self._limb_left = baxter_interface.Limb("left")
        self._limb_right = baxter_interface.Limb("right")
        self._gripper_left = baxter_interface.Gripper("left", CHECK_VERSION)
        self._gripper_right = baxter_interface.Gripper("right", CHECK_VERSION)
        self._io_left_lower = baxter_interface.DigitalIO('left_lower_button')
        self._io_left_upper = baxter_interface.DigitalIO('left_upper_button')
        self._io_right_lower = baxter_interface.DigitalIO('right_lower_button')
        self._io_right_upper = baxter_interface.DigitalIO('right_upper_button')
        self._navigator_io = baxter_interface.Navigator("right")

        # Verify Grippers Have No Errors and are Calibrated
        if self._gripper_left.error():
            self._gripper_left.reset()
        if self._gripper_right.error():
            self._gripper_right.reset()
        if (not self._gripper_left.calibrated() and
            self._gripper_left.type() != 'custom'):
            self._gripper_left.calibrate()
        if (not self._gripper_right.calibrated() and
            self._gripper_right.type() != 'custom'):
            self._gripper_right.calibrate()

    def _time_stamp(self):
        return self._time_shift + rospy.get_time() - self._start_time

    def pause(self, value):
        #pause recording if unpaused, unpause if paused
        if value:
            if self._pause:
                print("unpausing")
                self._start_time = rospy.get_time()
                self._pause=False 

            else:
                print("pausing")
                self.time_shift=self._time_stamp()
                self._pause=True

    def stop(self):
        """
        Stop recording.
        """
        self._done = True
    def button_stop(self, value):
        if value:
            self._done = True

    def done(self):
        """
        Return whether or not recording is done.
        """
        if rospy.is_shutdown():
            self.stop()
        return self._done
    def map_keyboard(self):
        left = baxter_interface.Limb('left')
        right = baxter_interface.Limb('right')
        grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
        grip_right = baxter_interface.Gripper('right', CHECK_VERSION)
        lj = left.joint_names()
        rj = right.joint_names()

        def set_j(limb, joint_name, delta):
            current_position = limb.joint_angle(joint_name)
            joint_command = {joint_name: current_position + delta}
            limb.set_joint_positions(joint_command)

        bindings = {
        #   key: (function, args, description)
            '9': (set_j, [left, lj[0], 0.1], "left_s0 increase"),
            '6': (set_j, [left, lj[0], -0.1], "left_s0 decrease"),
            '8': (set_j, [left, lj[1], 0.1], "left_s1 increase"),
            '7': (set_j, [left, lj[1], -0.1], "left_s1 decrease"),
            'o': (set_j, [left, lj[2], 0.1], "left_e0 increase"),
            'y': (set_j, [left, lj[2], -0.1], "left_e0 decrease"),
            'i': (set_j, [left, lj[3], 0.1], "left_e1 increase"),
            'u': (set_j, [left, lj[3], -0.1], "left_e1 decrease"),
            'l': (set_j, [left, lj[4], 0.1], "left_w0 increase"),
            'h': (set_j, [left, lj[4], -0.1], "left_w0 decrease"),
            'k': (set_j, [left, lj[5], 0.1], "left_w1 increase"),
            'j': (set_j, [left, lj[5], -0.1], "left_w1 decrease"),
            '.': (set_j, [left, lj[6], 0.1], "left_w2 increase"),
            'n': (set_j, [left, lj[6], -0.1], "left_w2 decrease"),
            ',': (grip_left.close, [], "left: gripper close"),
            'm': (grip_left.open, [], "left: gripper open"),
            '/': (grip_left.calibrate, [], "left: gripper calibrate"),
            'p': (self.pause, [self], "pause machine"),
           

            '4': (set_j, [right, rj[0], 0.1], "right_s0 increase"),
            '1': (set_j, [right, rj[0], -0.1], "right_s0 decrease"),
            '3': (set_j, [right, rj[1], 0.1], "right_s1 increase"),
            '2': (set_j, [right, rj[1], -0.1], "right_s1 decrease"),
            'r': (set_j, [right, rj[2], 0.1], "right_e0 increase"),
            'q': (set_j, [right, rj[2], -0.1], "right_e0 decrease"),
            'e': (set_j, [right, rj[3], 0.1], "right_e1 increase"),
            'w': (set_j, [right, rj[3], -0.1], "right_e1 decrease"),
            'f': (set_j, [right, rj[4], 0.1], "right_w0 increase"),
            'a': (set_j, [right, rj[4], -0.1], "right_w0 decrease"),
            'd': (set_j, [right, rj[5], 0.1], "right_w1 increase"),
            's': (set_j, [right, rj[5], -0.1], "right_w1 decrease"),
            'v': (set_j, [right, rj[6], 0.1], "right_w2 increase"),
            'z': (set_j, [right, rj[6], -0.1], "right_w2 decrease"),
            'c': (grip_right.close, [], "right: gripper close"),
            'x': (grip_right.open, [], "right: gripper open"),
            'b': (grip_right.calibrate, [], "right: gripper calibrate"),
         }
        done = False
       
        #while not done and not rospy.is_shutdown():
        c = baxter_external_devices.getch()
        if c:
            #catch Esc or ctrl-c
            if c in ['\x1b', '\x03']:
                self.stop()
                rospy.signal_shutdown("Example finished.")
            elif c in bindings:
                cmd = bindings[c]
                #expand binding to something like "set_j(right, 's0', 0.1)"
                cmd[0](*cmd[1])
                print("command: %s" % (cmd[2],))
            else:
                print("key bindings: ")
                print("  Esc: Quit")
                print("  ?: Help")
                for key, val in sorted(bindings.items(),
                                        key=lambda x: x[1][2]):
                    print("  %s: %s" % (key, val[2]))
    def record(self):
        """
        Records the current joint positions to a csv file if outputFilename was
        provided at construction this function will record the latest set of
        joint angles in a csv format.

        This function does not test to see if a file exists and will overwrite
        existing files.
        """
        left = baxter_interface.Limb('left')
        right = baxter_interface.Limb('right')
        grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
        grip_right = baxter_interface.Gripper('right', CHECK_VERSION)
        lj = left.joint_names()
        rj = right.joint_names()

        def set_j(limb, joint_name, delta):
            current_position = limb.joint_angle(joint_name)
            joint_command = {joint_name: current_position + delta}
            limb.set_joint_positions(joint_command)

        bindings = {
        #   key: (function, args, description)
            '9': (set_j, [left, lj[0], 0.1], "left_s0 increase"),
            '6': (set_j, [left, lj[0], -0.1], "left_s0 decrease"),
            '8': (set_j, [left, lj[1], 0.1], "left_s1 increase"),
            '7': (set_j, [left, lj[1], -0.1], "left_s1 decrease"),
            'o': (set_j, [left, lj[2], 0.1], "left_e0 increase"),
            'y': (set_j, [left, lj[2], -0.1], "left_e0 decrease"),
            'i': (set_j, [left, lj[3], 0.1], "left_e1 increase"),
            'u': (set_j, [left, lj[3], -0.1], "left_e1 decrease"),
            'l': (set_j, [left, lj[4], 0.1], "left_w0 increase"),
            'h': (set_j, [left, lj[4], -0.1], "left_w0 decrease"),
            'k': (set_j, [left, lj[5], 0.1], "left_w1 increase"),
            'j': (set_j, [left, lj[5], -0.1], "left_w1 decrease"),
            '.': (set_j, [left, lj[6], 0.1], "left_w2 increase"),
            'n': (set_j, [left, lj[6], -0.1], "left_w2 decrease"),
            ',': (grip_left.close, [], "left: gripper close"),
            'm': (grip_left.open, [], "left: gripper open"),
            '/': (grip_left.calibrate, [], "left: gripper calibrate"),
            'p': (self.pause, [self], "pause machine"),
           

            '4': (set_j, [right, rj[0], 0.1], "right_s0 increase"),
            '1': (set_j, [right, rj[0], -0.1], "right_s0 decrease"),
            '3': (set_j, [right, rj[1], 0.1], "right_s1 increase"),
            '2': (set_j, [right, rj[1], -0.1], "right_s1 decrease"),
            'r': (set_j, [right, rj[2], 0.1], "right_e0 increase"),
            'q': (set_j, [right, rj[2], -0.1], "right_e0 decrease"),
            'e': (set_j, [right, rj[3], 0.1], "right_e1 increase"),
            'w': (set_j, [right, rj[3], -0.1], "right_e1 decrease"),
            'f': (set_j, [right, rj[4], 0.1], "right_w0 increase"),
            'a': (set_j, [right, rj[4], -0.1], "right_w0 decrease"),
            'd': (set_j, [right, rj[5], 0.1], "right_w1 increase"),
            's': (set_j, [right, rj[5], -0.1], "right_w1 decrease"),
            'v': (set_j, [right, rj[6], 0.1], "right_w2 increase"),
            'z': (set_j, [right, rj[6], -0.1], "right_w2 decrease"),
            'c': (grip_right.close, [], "right: gripper close"),
            'x': (grip_right.open, [], "right: gripper open"),
            'b': (grip_right.calibrate, [], "right: gripper calibrate"),
         }
        if self._filename:
            joints_left = self._limb_left.joint_names()
            joints_right = self._limb_right.joint_names()
            with open(self._filename, 'w') as f:
                f.write('time,')
                f.write(','.join([j for j in joints_left]) + ',')
                f.write('left_gripper,')
                f.write(','.join([j for j in joints_right]) + ',')
                f.write('right_gripper\n')
                self._navigator_io.button0_changed.connect(self.pause)
                self._navigator_io.button2_changed.connect(self.button_stop)
                #self.map_keyboard()
                print("Controlling joints. Press ? for help, Esc to quit.")
                while not self.done():
                    # Look for gripper button presses
                    #print(self.pause)
                   # print(self._pause and not self.done())
                    c = baxter_external_devices.getch()
                    while self._pause and not self.done():
                        if self._io_left_lower.state:
                            self._gripper_left.open()
                        elif self._io_left_upper.state:
                            self._gripper_left.close()
                        if self._io_right_lower.state:
                            self._gripper_right.open()
                        elif self._io_right_upper.state:
                            self._gripper_right.close()
                        if c:
                            #catch Esc or ctrl-c
                            if c in ['\x1b', '\x03']:
                                self.stop()
                                rospy.signal_shutdown("Example finished.")
                            elif c in bindings:
                                cmd = bindings[c]
                                #expand binding to something like "set_j(right, 's0', 0.1)"
                                cmd[0](*cmd[1])
                                print("command: %s" % (cmd[2],))
                            else:
                                print("key bindings: ")
                                print("  Esc: Quit")
                                print("  ?: Help")
                                for key, val in sorted(bindings.items(),
                                                        key=lambda x: x[1][2]):
                                    print("  %s: %s" % (key, val[2]))
                        #self.map_keyboard()
                        #print("i'm stuck")
                        #pass 
                    if self._io_left_lower.state:
                        self._gripper_left.open()
                    elif self._io_left_upper.state:
                        self._gripper_left.close()
                    if self._io_right_lower.state:
                        self._gripper_right.open()
                    elif self._io_right_upper.state:
                        self._gripper_right.close()
                    if c:
                        #catch Esc or ctrl-c
                        if c in ['\x1b', '\x03']:
                            self.stop()
                            rospy.signal_shutdown("Example finished.")
                        elif c in bindings:
                            cmd = bindings[c]
                            #expand binding to something like "set_j(right, 's0', 0.1)"
                            cmd[0](*cmd[1])
                            print("command: %s" % (cmd[2],))
                        else:
                            print("key bindings: ")
                            print("  Esc: Quit")
                            print("  ?: Help")
                            for key, val in sorted(bindings.items(),
                                                    key=lambda x: x[1][2]):
                                print("  %s: %s" % (key, val[2]))



                    #self.map_keyboard()
                    angles_left = [self._limb_left.joint_angle(j)
                                   for j in joints_left]
                    angles_right = [self._limb_right.joint_angle(j)
                                    for j in joints_right]

                    f.write("%f," % (self._time_stamp(),))

                    f.write(','.join([str(x) for x in angles_left]) + ',')
                    f.write(str(self._gripper_left.position()) + ',')

                    f.write(','.join([str(x) for x in angles_right]) + ',')
                    f.write(str(self._gripper_right.position()) + '\n')

                    self._rate.sleep()
