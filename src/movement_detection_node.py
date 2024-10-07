#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

def callback(cmd_vel_msg):
    linear_x = cmd_vel_msg.linear.x
    angular_z = cmd_vel_msg.angular.z
    movement = ""

    if linear_x > 0.01 and angular_z < -0.01:
        movement = "turnright"
    elif linear_x > 0.01 and angular_z > 0.01:
        movement = "turnleft"
    elif linear_x < -0.01 and angular_z > 0.01:
        movement = "turnright_backward"
    elif linear_x < -0.01 and angular_z < -0.01:
        movement = "turnleft_backward"
    elif angular_z > 0.01:
        movement = "rotateright"
    elif angular_z < -0.01:
        movement = "rotateleft"
    elif linear_x < -0.01 and -0.01 <= angular_z <= 0.01:
        movement = "move_backward"
    elif linear_x > 0.01 and -0.01 <= angular_z <= 0.01:
        movement = "move_forward"    
    else:
        movement = "stationary"  # default when no movement matches

    # Publish the movement status
    pub.publish(movement)
    rospy.loginfo(f"Movement detected: {movement}")

def listener():
    rospy.init_node('movement_detection_node', anonymous=True)

    # Subscribe to the /cmd_vel topic
    rospy.Subscriber("/cmd_vel", Twist, callback)

    # Publisher for the movement status
    global pub
    pub = rospy.Publisher('/movement_status', String, queue_size=10)

    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
