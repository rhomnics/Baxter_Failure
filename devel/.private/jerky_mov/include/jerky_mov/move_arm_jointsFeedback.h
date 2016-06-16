// Generated by gencpp from file jerky_mov/move_arm_jointsFeedback.msg
// DO NOT EDIT!


#ifndef JERKY_MOV_MESSAGE_MOVE_ARM_JOINTSFEEDBACK_H
#define JERKY_MOV_MESSAGE_MOVE_ARM_JOINTSFEEDBACK_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace jerky_mov
{
template <class ContainerAllocator>
struct move_arm_jointsFeedback_
{
  typedef move_arm_jointsFeedback_<ContainerAllocator> Type;

  move_arm_jointsFeedback_()
    : percent_complete(0.0)  {
    }
  move_arm_jointsFeedback_(const ContainerAllocator& _alloc)
    : percent_complete(0.0)  {
  (void)_alloc;
    }



   typedef float _percent_complete_type;
  _percent_complete_type percent_complete;




  typedef boost::shared_ptr< ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator> const> ConstPtr;

}; // struct move_arm_jointsFeedback_

typedef ::jerky_mov::move_arm_jointsFeedback_<std::allocator<void> > move_arm_jointsFeedback;

typedef boost::shared_ptr< ::jerky_mov::move_arm_jointsFeedback > move_arm_jointsFeedbackPtr;
typedef boost::shared_ptr< ::jerky_mov::move_arm_jointsFeedback const> move_arm_jointsFeedbackConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace jerky_mov

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'std_msgs': ['/opt/ros/indigo/share/std_msgs/cmake/../msg'], 'sensor_msgs': ['/opt/ros/indigo/share/sensor_msgs/cmake/../msg'], 'actionlib_msgs': ['/opt/ros/indigo/share/actionlib_msgs/cmake/../msg'], 'geometry_msgs': ['/opt/ros/indigo/share/geometry_msgs/cmake/../msg'], 'jerky_mov': ['/home/rhomni/bax_ws/bax_local/devel/.private/jerky_mov/share/jerky_mov/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator> >
{
  static const char* value()
  {
    return "d342375c60a5a58d3bc32664070a1368";
  }

  static const char* value(const ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xd342375c60a5a58dULL;
  static const uint64_t static_value2 = 0x3bc32664070a1368ULL;
};

template<class ContainerAllocator>
struct DataType< ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator> >
{
  static const char* value()
  {
    return "jerky_mov/move_arm_jointsFeedback";
  }

  static const char* value(const ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n\
#feedback\n\
float32 percent_complete\n\
";
  }

  static const char* value(const ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.percent_complete);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER;
  }; // struct move_arm_jointsFeedback_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::jerky_mov::move_arm_jointsFeedback_<ContainerAllocator>& v)
  {
    s << indent << "percent_complete: ";
    Printer<float>::stream(s, indent + "  ", v.percent_complete);
  }
};

} // namespace message_operations
} // namespace ros

#endif // JERKY_MOV_MESSAGE_MOVE_ARM_JOINTSFEEDBACK_H