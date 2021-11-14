#! /usr/bin/env python3
# Sinusoidal function trajectory

import rospy
from rospy.timer import Rate
from std_msgs.msg import Float64
import numpy as np


t = np.arange(0, 60, 0.6)

def sine(t):
    sine = np.sin(t/10)
    return sine

s = sine(t)


def talker():
    global error, client, pub1, rate
    rospy.init_node("test_pids")
    
    command_path = "/arm/motor_end_effector_position_controller/command"

    # pub1: publishes end_effector's position
    pub1 = rospy.Publisher(command_path, Float64, queue_size=10)
    rate = rospy.Rate(1.66)

    
    while not rospy.is_shutdown():
        for i in s:
            pub1.publish(i)
            rate.sleep()
            

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass