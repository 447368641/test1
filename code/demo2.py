#!/usr/bin/env python

import os
import rospy
from duckietown import DTROS
#duckie bot API:Motors
from duckietown_msgs.msg import WheelsCmdStamped, BoolStamped,String, LEDPattern
from duckietown_msgs.srv import SetCustomLEDPattern, ChangePattern
from std_msgs.msg import String
from time import sleep

class Demo2(DTROS):

    def __init__(self,node_name):
        super(Demo1,self).__init__(node_name=node_name)
        self.wheelpub = rospy.Publisher(
            '/duckiebot3/wheels_driver_node/wheels_cmd',
            WheelsCmdStamped,
            queue_size=1)
	
	self.speed = 0.5#within -1.0~1.0

    def forward(self,time):
#        print "Forward"
        msg = WheelsCmdStamped()
        msg.header.stamp = rospy.get_rostime()
        msg.vel_left = self.speed
        msg.vel_right = self.speed
        self.wheelpub.publish(msg)

        self.set_leds("forward")
        rospy.sleep(time)

    def left_turn(self,time):
        msg = WheelsCmdStamped()
        msg.header.stamp = rospy.get_rostime()
        msg.vel_left = self.speed
        msg.vel_right = self.speed + 0.3
        self.wheelpub.publish(msg)
        
        self.set_leds("left_turn")
        rospy.sleep(time)



        

    def right_turn(self,time):
        msg = WheelsCmdStamped()
        msg.header.stamp = rospy.get_rostime()
        msg.vel_left = self.speed + 0.3
        msg.vel_right = self.speed
        self.wheelpub.publish(msg)
        
        self.set_leds("right_turn")
        rospy.sleep(time)


    def rotate(self,time):
#        print "Rotate"
        msg = WheelsCmdStamped()
        msg.header.stamp = rospy.get_rostime()
        msg.vel_left = self.speed
        msg.vel_right = -self.speed
        self.wheelpub.publish(msg)
        rospy.sleep(time)

    def stop(self):
        msg = WheelsCmdStamped()
        msg.header.stamp = rospy.get_rostime()
        msg.vel_left = 0.0
        msg.vel_right = 0.0
        self.wheelpub.publish(msg)        
        self.set_leds("stop")
        


    def set_leds(self,mode):
        rospy.wait_for_service('/duckiebot3/led_emitter_node/set_custom_pattern')
        try:
            service = rospy.ServiceProxy('/duckiebot3/led_emitter_node/set_custom_pattern',
                                         SetCustomLEDPattern)
            msg = LEDPattern()
            msg.color_list = ['white', 'switchedoff', 'white', 'switchedoff', 'white']
            msg.color_mask = [1, 1, 1, 1, 1]
            msg.frequency = 0
            msg.frequency_mask = [0, 0, 0, 0, 0]
            
            if mode == "stop":
                msg.color_list[1] = 'red'
                msg.color_list[3] = 'red'
            elif mode == "left_turn":
                msg.color_list[1] = 'yellow'
                msg.frequency = 1.0
                msg.frequency_mask[1] = 1
            elif mode == "right_turn":
                msg.frequency = 1.0
                msg.color_list[3] = 'yellow'
                msg.frequency_mask[3] = 1
            else:
                pass
            
            response = service(msg)
            rospy.loginfo(response)
            
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e


    def run(self):
        rospy.sleep(2)
        self.forward(2)
        self.left_turn(2)
        self.right_turn(2)
        self.stop()


if __name__ == '__main__':
    node = Demo2(node_name="demo2")
    node.run()
    node.spin()
