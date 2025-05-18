#!/usr/bin/env python

import rospy
import actionlib
import time
from section2.msg import OdomRecordAction, OdomRecordFeedback, OdomRecordResult
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point32
from math import sqrt, pow

class RecordOdometry(object):
    # Creating some initial class parameters
    _feedback = OdomRecordFeedback()
    _result = OdomRecordResult()
    position_x = 0.0
    position_y = 0.0
    orientation_theta = 0.0
    _dist_one_lap = 5.5
   
    # Constructor
    def __init__(self):
        # Creating some object parameters
        rospy.loginfo("Initializing the action server.")
        # Action server

        self._as = actionlib.SimpleActionServer("record_odometry_server", OdomRecordAction, execute_cb = self.goal_callback, auto_start = False)
        self._as.start()
        self.rate = rospy.Rate(1)
        rospy.loginfo("Action server initalized.")

        # Subscriber
        rospy.loginfo("Creating /odom subscriber...")
        _sub_odom = rospy.Subscriber("/odom", Odometry, callback = self.odom_callback)
        while _sub_odom.get_num_connections() < 1:
            pass

        rospy.loginfo("/odom subscriber created.")


    # Server callback
    def goal_callback(self, goal):
     #result = OdomRecordResult()
     
     rate = rospy.Rate(2)
     dist = 0.0  # Travelled distance
     success = True
     i = 0
    
     while dist <= self._dist_one_lap:
         rospy.loginfo("Saving odometry readings.")
         # Check if the goal is cancelled
         if self._as.is_preempt_requested():
            success = False
            self._as.set_preempted()
            break
        
         # Saving odometry readings
         self._odom_readings = Point32()
         self._odom_readings.x = self.position_x
         self._odom_readings.y = self.position_y
         self._odom_readings.z = self.orientation_theta
        
         self._result.list_of_odoms.append(self._odom_readings)
         print(self._result.list_of_odoms)
        
         if i <=1:
             self._feedback.current_total = 0
         else:
             # Travelled distance
             dist += sqrt( pow( self._result.list_of_odoms[i].x - self._result.list_of_odoms[i-1].x, 2) + pow( self._result.list_of_odoms[i].y - self._result.list_of_odoms[i-1].y, 2) )
             #dist += 0.25  # Just to evolve the distance
             self._feedback.current_total = dist

         self._as.publish_feedback(self._feedback)


         # loop variables
         i += 1
         rate.sleep()
         #time.sleep(2)

     if success:
        self._as.set_succeeded(self._result)
        rospy.loginfo("Finishing the action server.")


    # Odometry callback
    def odom_callback(self, msg):
     self.position_x = msg.pose.pose.position.x
     self.position_y = msg.pose.pose.position.y
     self.orientation_theta = msg.pose.pose.orientation.z

def main():
     rospy.init_node("record_odometry_server_node")
     RecordOdometry()
     rospy.spin()
  
if __name__ == '__main__':
    rospy.init_node("record_odometry_server_node")
    RecordOdometry()
    rospy.spin()