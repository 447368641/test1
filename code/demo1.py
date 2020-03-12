#!/usr/bin/env python

import os
import rospy
from duckietown import DTROS
#duckie bot API:Motors
from duckietown_msgs.msg import WheelsCmdStamped, BoolStamped
from std_msgs.msg import String
from time import sleep

class Demo1(DTROS):


    def __init__(self,node_name):
        super(Demo1,self).__init__(node_name=node_name)

        self.wheelpub = rospy.Publisher(
            '/duckiebot3/wheels_driver_node/wheels_cmd',
            WheelsCmdStamped,
            queue_size=1)


    def forward(self,velocity,time):
#        print "Forward"
        msg = WheelsCmdStamped()
        msg.header.stamp = rospy.get_rostime()
        msg.vel_left = velocity
        msg.vel_right = velocity
        self.wheelpub.publish(msg)
        rospy.sleep(time)



    def rotate(self,velocity,time):
#        print "Rotate"
        msg = WheelsCmdStamped()
        msg.header.stamp = rospy.get_rostime()
        msg.vel_left = velocity
        msg.vel_right = -velocity
        self.wheelpub.publish(msg)
        rospy.sleep(time)


    def stop(self):
        msg = WheelsCmdStamped()
        msg.header.stamp = rospy.get_rostime()
        msg.vel_left = 0.0
        msg.vel_right = 0.0
        self.wheelpub.publish(msg)


    def run(self):
        rospy.sleep(2)
        self.forward(0.6,2)
        self.rotate(0.5,0.5)
        self.forward(0.6,2)
        self.stop()




if __name__ == '__main__':
    node = Demo1(node_name="demo1")
    node.run()
    node.spin()
