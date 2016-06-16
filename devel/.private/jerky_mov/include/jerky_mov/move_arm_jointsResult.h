// Generated by gencpp from file jerky_mov/move_arm_jointsResult.msg
// DO NOT EDIT!


#ifndef JERKY_MOV_MESSAGE_MOVE_ARM_JOINTSRESULT_H
#define JERKY_MOV_MESSAGE_MOVE_ARM_JOINTSRESULT_H


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
struct move_arm_jointsResult_
{
  typedef move_arm_jointsResult_<ContainerAllocator> Type;

  move_arm_jointsResult_()
    : complete(false)  {
    }
  move_arm_jointsResult_(const ContainerAllocator& _alloc)
    : complete(false)  {
  (void)_alloc;
    }



   typedef uint8_t _complete_type;
  _complete_type complete;




  typedef boost::shared_ptr< ::jerky_mov::move_arm_jointsResult_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::jerky_mov::move_arm_jointsResult_<ContainerAllocator> const> ConstPtr;

}; // struct move_arm_jointsResult_

typedef ::jerky_mov::move_arm_jointsResult_<std::allocator<void> > move_arm_jointsResult;

typedef boost::shared_ptr< ::jerky_mov::move_arm_jointsResult > move_arm_jointsResultPtr;
typedef boost::shared_ptr< ::jerky_mov::move_arm_jointsResult const> move_arm_jointsResultConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::jerky_mov::move_arm_jointsResult_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::jerky_mov::move_arm_jointsResult_<ContainerAllocator> >::stream(s, "", v);
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
struct IsFixedSize< ::jerky_mov::move_arm_jointsResult_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::jerky_mov::move_arm_jointsResult_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::jerky_mov::move_arm_jointsResult_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::jerky_mov::move_arm_jointsResult_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::jerky_mov::move_arm_jointsResult_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::jerky_mov::move_arm_jointsResult_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::jerky_mov::move_arm_jointsResult_<ContainerAllocator> >
{
  static const char* value()
  {
    return "9d8061d2347621a6ed88451e28811cc7";
  }

  static const char* value(const ::jerky_mov::move_arm_jointsResult_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x9d8061d2347621a6ULL;
  static const uint64_t static_value2 = 0xed88451e28811cc7ULL;
};

template<class ContainerAllocator>
struct DataType< ::jerky_mov::move_arm_jointsResult_<ContainerAllocator> >
{
  static const char* value()
  {
    return "jerky_mov/move_arm_jointsResult";
  }

  static const char* value(const ::jerky_mov::move_arm_jointsResult_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::jerky_mov::move_arm_jointsResult_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n\
#result definition\n\
bool complete\n\
\n\
";
  }

  static const char* value(const ::jerky_mov::move_arm_jointsResult_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::jerky_mov::move_arm_jointsResult_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.complete);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER;
  }; // struct move_arm_jointsResult_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::jerky_mov::move_arm_jointsResult_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::jerky_mov::move_arm_jointsResult_<ContainerAllocator>& v)
  {
    s << indent << "complete: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.complete);
  }
};

} // namespace message_operations
} // namespace ros

#endif // JERKY_MOV_MESSAGE_MOVE_ARM_JOINTSRESULT_H