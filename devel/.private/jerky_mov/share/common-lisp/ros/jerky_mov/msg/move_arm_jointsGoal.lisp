; Auto-generated. Do not edit!


(cl:in-package jerky_mov-msg)


;//! \htmlinclude move_arm_jointsGoal.msg.html

(cl:defclass <move_arm_jointsGoal> (roslisp-msg-protocol:ros-message)
  ((joints
    :reader joints
    :initarg :joints
    :type (cl:vector sensor_msgs-msg:JointState)
   :initform (cl:make-array 0 :element-type 'sensor_msgs-msg:JointState :initial-element (cl:make-instance 'sensor_msgs-msg:JointState)))
   (type
    :reader type
    :initarg :type
    :type cl:fixnum
    :initform 0)
   (wait
    :reader wait
    :initarg :wait
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass move_arm_jointsGoal (<move_arm_jointsGoal>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <move_arm_jointsGoal>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'move_arm_jointsGoal)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name jerky_mov-msg:<move_arm_jointsGoal> is deprecated: use jerky_mov-msg:move_arm_jointsGoal instead.")))

(cl:ensure-generic-function 'joints-val :lambda-list '(m))
(cl:defmethod joints-val ((m <move_arm_jointsGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader jerky_mov-msg:joints-val is deprecated.  Use jerky_mov-msg:joints instead.")
  (joints m))

(cl:ensure-generic-function 'type-val :lambda-list '(m))
(cl:defmethod type-val ((m <move_arm_jointsGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader jerky_mov-msg:type-val is deprecated.  Use jerky_mov-msg:type instead.")
  (type m))

(cl:ensure-generic-function 'wait-val :lambda-list '(m))
(cl:defmethod wait-val ((m <move_arm_jointsGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader jerky_mov-msg:wait-val is deprecated.  Use jerky_mov-msg:wait instead.")
  (wait m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <move_arm_jointsGoal>) ostream)
  "Serializes a message object of type '<move_arm_jointsGoal>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'joints))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'joints))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'type)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'wait) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <move_arm_jointsGoal>) istream)
  "Deserializes a message object of type '<move_arm_jointsGoal>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'joints) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'joints)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'sensor_msgs-msg:JointState))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'type)) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'wait) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<move_arm_jointsGoal>)))
  "Returns string type for a message object of type '<move_arm_jointsGoal>"
  "jerky_mov/move_arm_jointsGoal")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'move_arm_jointsGoal)))
  "Returns string type for a message object of type 'move_arm_jointsGoal"
  "jerky_mov/move_arm_jointsGoal")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<move_arm_jointsGoal>)))
  "Returns md5sum for a message object of type '<move_arm_jointsGoal>"
  "298cc92a24d31028fd232a9184a416b7")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'move_arm_jointsGoal)))
  "Returns md5sum for a message object of type 'move_arm_jointsGoal"
  "298cc92a24d31028fd232a9184a416b7")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<move_arm_jointsGoal>)))
  "Returns full string definition for message of type '<move_arm_jointsGoal>"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%#goal definition~%sensor_msgs/JointState[] joints~%uint8 type~%bool wait~%~%~%================================================================================~%MSG: sensor_msgs/JointState~%# This is a message that holds data to describe the state of a set of torque controlled joints. ~%#~%# The state of each joint (revolute or prismatic) is defined by:~%#  * the position of the joint (rad or m),~%#  * the velocity of the joint (rad/s or m/s) and ~%#  * the effort that is applied in the joint (Nm or N).~%#~%# Each joint is uniquely identified by its name~%# The header specifies the time at which the joint states were recorded. All the joint states~%# in one message have to be recorded at the same time.~%#~%# This message consists of a multiple arrays, one for each part of the joint state. ~%# The goal is to make each of the fields optional. When e.g. your joints have no~%# effort associated with them, you can leave the effort array empty. ~%#~%# All arrays in this message should have the same size, or be empty.~%# This is the only way to uniquely associate the joint name with the correct~%# states.~%~%~%Header header~%~%string[] name~%float64[] position~%float64[] velocity~%float64[] effort~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'move_arm_jointsGoal)))
  "Returns full string definition for message of type 'move_arm_jointsGoal"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%#goal definition~%sensor_msgs/JointState[] joints~%uint8 type~%bool wait~%~%~%================================================================================~%MSG: sensor_msgs/JointState~%# This is a message that holds data to describe the state of a set of torque controlled joints. ~%#~%# The state of each joint (revolute or prismatic) is defined by:~%#  * the position of the joint (rad or m),~%#  * the velocity of the joint (rad/s or m/s) and ~%#  * the effort that is applied in the joint (Nm or N).~%#~%# Each joint is uniquely identified by its name~%# The header specifies the time at which the joint states were recorded. All the joint states~%# in one message have to be recorded at the same time.~%#~%# This message consists of a multiple arrays, one for each part of the joint state. ~%# The goal is to make each of the fields optional. When e.g. your joints have no~%# effort associated with them, you can leave the effort array empty. ~%#~%# All arrays in this message should have the same size, or be empty.~%# This is the only way to uniquely associate the joint name with the correct~%# states.~%~%~%Header header~%~%string[] name~%float64[] position~%float64[] velocity~%float64[] effort~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <move_arm_jointsGoal>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'joints) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
     1
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <move_arm_jointsGoal>))
  "Converts a ROS message object to a list"
  (cl:list 'move_arm_jointsGoal
    (cl:cons ':joints (joints msg))
    (cl:cons ':type (type msg))
    (cl:cons ':wait (wait msg))
))
