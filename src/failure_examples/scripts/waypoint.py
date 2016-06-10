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
Baxter RSDK Joint Position Waypoints Example
"""
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


class Waypoints(object):
    def __init__(self, limb, filename, speed, accuracy):
        # Create baxter_interface limb instance
        self._arm = limb
        self.file=filename
        self._limb = baxter_interface.Limb(self._arm)
        self.result = [False, '']

        # Parameters which will describe joint position moves
        self._speed = speed
        self._accuracy = accuracy

        #activate all limbs
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




        # Recorded waypoints
        self._waypoints = list()

        # Recording state
        self._is_recording = False

        # Verify robot is enabled
        print("Getting robot state... ")
        self._rs = baxter_interface.RobotEnable()
        self._init_state = self._rs.state().enabled
        print("Enabling robot... ")
        self._rs.enable()

        # Create Navigator I/O
        self._navigator_io = baxter_interface.Navigator(self._arm)

    def _record_waypoint(self, value):
        """
        Stores joint position waypoints

        Navigator 'OK/Wheel' button callback
        """
        print("Waypoint New")
        if value:
            print("Waypoint Recorded")
            self._waypoints.append(self._limb_left.joint_angles())
            self._waypoints.append(self._limb_right.joint_angles())

    def _stop_recording(self, value):
        """
        Sets is_recording to false

        Navigator 'Rethink' button callback
        """
        # On navigator Rethink button press, stop recording
        print("Outside If")
        if value:
            print("Stop Recording")
            self._is_recording = False

    def record(self):
        """
        Records joint position waypoints upon each Navigator 'OK/Wheel' button
        press.
        """
        rospy.loginfo("Waypoint Recording Started")
        print("Press Navigator 'OK/Wheel' button to record a new joint "
        "joint position waypoint.")
        print("Press Navigator 'Rethink' button when finished recording "
              "waypoints to begin playback")
        # Connect Navigator I/O signals
        # Navigator scroll wheel button press
        self._navigator_io.button0_changed.connect(self._record_waypoint)
        # Navigator Rethink button press
        self._navigator_io.button2_changed.connect(self._stop_recording)

        # Set recording flag
        self._is_recording = True

        # Loop until waypoints are done being recorded ('Rethink' Button Press)
        while self._is_recording and not rospy.is_shutdown():
            rospy.sleep(1.0)

        with open(self.file, 'wb') as f:
            f.write(json.dumps(self._waypoints))
            #f.write(self.file + '\n')
            #for waypoint in self._waypoints:
            #    f.write(str(waypoint) + '\n')

        # We are now done with the navigator I/O signals, disconnecting them
        print("Disconnecting buttons")
        self._navigator_io.button0_changed.disconnect(self._record_waypoint)
        self._navigator_io.button2_changed.disconnect(self._stop_recording)
        print("Buttons Disconnected")

    def return_failure(self, trace):
        """Commonly used failure return
        """
        self.result[0] = False
        self.result[1] = trace
        try:
            self._rs.disable()
        except Exception:
            pass

    def move_thread(self, limb, angle, queue, timeout=15.0):
        try:
            print(str(limb) + "this the the limb \n")
            print(str(angle)+ "this is the  pos \n")
            limb.move_to_joint_positions(angle, timeout)
            print("move left")
            queue.put(None)
        except Exception, exception:
            queue.put(traceback.format_exc())
            queue.put(exception)
            """
            Threaded joint movement allowing for simultaneous joint moves.
            """
        #try:
        #    limb.move_to_joint_positions(angle, timeout)
        #    queue.put(None)
        #except Exception, exception:
        #    queue.put(traceback.format_exc())
        #    queue.put(exception)

    def playback(self):
        """
        Loops playback of recorded joint position waypoints until program is
        exited
        """
        rospy.sleep(1.0)
        #if True:
        try:
            rospy.loginfo("Waypoint Playback Started")
            print("  Press Ctrl-C to stop...")
            left_queue = Queue.Queue()
            right_queue = Queue.Queue()
            right = self._limb_right
            left = self._limb_left
            print(str(left) + "this the the left \n")

            # Set joint position speed ratio for execution
            self._limb.set_joint_position_speed(self._speed)
            source_file = open(self.file, 'rb').read()
            waypoints=json.loads(source_file)
            left_waypoints=list()
            right_waypoints=list()
            for idx, waypoint in enumerate(waypoints):
                if idx%2==0:
                    left_waypoints.append(waypoint)
                else:
                    right_waypoints.append(waypoint)

            # Loop until program is exited
            loop = 0
            while not rospy.is_shutdown():
                loop += 1
                print("Waypoint playback loop #%d " % (loop,))
                for lw, rw in zip(left_waypoints, right_waypoints):
                    if rospy.is_shutdown():
                        break
                    print(str(lw)+'\n')
                    print(str(rw)+'\n')
                    zl=dict(zip(left.joint_names(), lw))
                    zr=dict(zip(right.joint_names(), rw))
                    print(str(zl)+ "this is the  left pos \n")

                    left_thread = threading.Thread(
                        target=self.move_thread,
                        args=(self._limb_left,
                              lw,
                              left_queue
                              )
                    )
                    print("made left thread")
                    right_thread = threading.Thread(
                        target=self.move_thread,
                        args=(self._limb_right,
                              rw,
                              right_queue
                              )
                    )
                    left_thread.daemon = True
                    right_thread.daemon = True
                    left_thread.start()
                    right_thread.start()
                    baxter_dataflow.wait_for(
                        lambda: not (left_thread.is_alive() or
                                     right_thread.is_alive()),
                        timeout=20.0,
                        timeout_msg=("Timeout while waiting for arm move threads"
                                     " to finish"),
                        rate=10,
                    )
                    left_thread.join()
                    right_thread.join()
                    result = left_queue.get()
                    if not result is None:
                        print(str(left_queue.get()) + "this is an error \n")
                        raise left_queue.get()
                    result = right_queue.get()
                    if not result is None:
                        raise right_queue.get()
                    rospy.sleep(1.0)
                # Sleep for a few seconds between playback loops
                rospy.sleep(3.0)
        except Exception:
            print("i have failed")
            self.return_failure(traceback.format_exc())

        # Set joint position speed back to default
        self._limb.set_joint_position_speed(0.3)

    def clean_shutdown(self):
        print("\nExiting example...")
        if not self._init_state:
            print("Disabling robot...")
            self._rs.disable()
        return True


def main():
    """RSDK Joint Position Waypoints Example

    Records joint positions each time the navigator 'OK/wheel'
    button is pressed.
    Upon pressing the navigator 'Rethink' button, the recorded joint positions
    will begin playing back in a loop.
    """
    arg_fmt = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=arg_fmt,
                                     description=main.__doc__)
    required = parser.add_argument_group('required arguments')
    parser.add_argument(
        '-l', '--limb', choices=['left', 'right'], default='right',
        help='limb to record/playback waypoints'
    )
    required.add_argument(
        '-f', '--file', dest='filename', required=True,
        help='the file name to record to'
    )
    parser.add_argument(
        '-s', '--speed', default=0.3, type=float,
        help='joint position motion speed ratio [0.0-1.0] (default:= 0.3)'
    )
    parser.add_argument(
        '-a', '--accuracy',
        default=baxter_interface.settings.JOINT_ANGLE_TOLERANCE, type=float,
        help='joint position accuracy (rad) at which waypoints must achieve'
    )

    parser.add_argument(
        '-m', '--mode', choices=['record', 'play', 'both'], default='both', 
        help='choose whether you want to record some waypoints or play them back or both'
    )
    args = parser.parse_args(rospy.myargv()[1:])

    print("Initializing node... ")
    rospy.init_node("rsdk_joint_position_waypoints_%s" % (args.limb,))

    waypoints = Waypoints(args.limb, args.filename, args.speed, args.accuracy)

    # Register clean shutdown
    rospy.on_shutdown(waypoints.clean_shutdown)

    # Begin example program
    if args.mode !='play':
        waypoints.record()
    
    if args.mode !='record':
        print("Now Entering Playback Method")
        waypoints.playback()

if __name__ == '__main__':
    main()
