#! /usr/bin/env python

import rospy
from std_msgs.msg import Header
from std_msgs.msg import Float64
import numpy as np
import matplotlib.pyplot as plt

def talker():
    rospy.init_node('posicion')

    pub_1 = rospy.Publisher('/biped/torso_link_RHYaw_link_position_controller/command', Float64, queue_size=10)
    pub_2 = rospy.Publisher('/biped/RHYaw_link_RHRoll_link_position_controller/command', Float64, queue_size=10)
    pub_3 = rospy.Publisher('/biped/RHRoll_link_RHPitch_link_position_controller/command', Float64, queue_size=10)    
    pub_4 = rospy.Publisher('/biped/RHPitch_link_RKPitch_link_position_controller/command', Float64, queue_size=10)
    pub_5 = rospy.Publisher('/biped/RKPitch_link_RAPitch_link_position_controller/command', Float64, queue_size=10)
    pub_6 = rospy.Publisher('/biped/RAPitch_link_RARoll_link_position_controller/command', Float64, queue_size=10)
    
    pub_7 = rospy.Publisher('/biped/torso_link_LHYaw_link_position_controller/command', Float64, queue_size=10)
    pub_8 = rospy.Publisher('/biped/LHYaw_link_LHRoll_link_position_controller/command', Float64, queue_size=10)    
    pub_9 = rospy.Publisher('/biped/LHRoll_link_LHPitch_link_position_controller/command', Float64, queue_size=10)
    pub_10 = rospy.Publisher('/biped/LHPitch_link_LKPitch_link_position_controller/command', Float64, queue_size=10)
    pub_11 = rospy.Publisher('/biped/LKPitch_link_LAPitch_link_position_controller/command', Float64, queue_size=10)
    pub_12 = rospy.Publisher('/biped/LAPitch_link_LARoll_link_position_controller/command', Float64, queue_size=10)
    
    rate = rospy.Rate(50) # 10hz

    #q.name = ['torso_link_RHYaw_link','RHYaw_link_RHRoll_link','RHRoll_link_RHPitch_link','RHPitch_link_RKPitch_link','RKPitch_link_RAPitch_link','RAPitch_link_RARoll_link',
    #'torso_LHYaw_link','LHYaw_link_LHRoll_link','LHRoll_link_LHPitch_link','LHPitch_link_LKPitch_link','LKPitch_link_LAPitch_link','LAPitch_link_LARoll_link']
    # q.position[0] = 
    # q.position[1] = 
    # q.position[2] = 
    # q.position[3] = 
    # q.position[4] = 
    # q.position[5] = 
    # q.position[6] = 
    # q.position[7] = 
    # q.position[8] = 
    # q.position[9] = 
    # q.position[10] = 
    #q.position[:] = [ 0.02119545,-0.        ,-0.07858764, 0.15717528,-0.09302034,-0.00481323, 0.01532651,-0.        ,-0.07858764, 0.15717528,-0.0886152 , 0.01508163]

    s = Float64()

    while not rospy.is_shutdown():
        with open('trayectorias7.txt') as f:
            for linea in f:
                s = np.fromstring(linea, dtype=float, sep=',')
                pub_1.publish(s[0])
                pub_2.publish(s[1])
                pub_3.publish(s[2])
                pub_4.publish(s[3])
                pub_5.publish(s[4])
                pub_6.publish(s[5])
                
                pub_7.publish(s[6])
                pub_8.publish(s[7])
                pub_9.publish(s[8])
                pub_10.publish(s[9])
                pub_11.publish(s[10])
                pub_12.publish(s[11])

                #plt.plot(s)
                #plt.show()

                rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
