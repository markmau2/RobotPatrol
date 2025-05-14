#!/usr/bin/env python

import rospy
import actionlib

from section2.msg import OdomRecordAction, OdomRecordFeedback, OdomRecordResult
from nav_msgs.msg import Odometry
from numpy import sqrt

class RecordOdometry(object):
    # Creating some initial class parameters
    _feedback = OdomRecordFeedback()
    _result = OdomRecordResult()
    position_x = 0.0
    position_y = 0.0
    orientation_theta = 0.0
    _dist_one_lap = 1.0


    # Constructor
    def __init__(self):
        # Creating some object parameters
        rospy.loginfo("Initializing the action server.")
        # Action server
        self._as = actionlib.SimpleActionServer("record_odometry_server", OdomRecordAction, execute_cb=self.goal_callback, auto_start=False)
        self._as.start()
        rospy.loginfo("Action server initalized.")

        # Subscriber
        rospy.loginfo("Creating /odom subscriber...")
        _sub_odom = rospy.Subscriber("/odom", Odometry, self.odom_callback)
        while _sub_odom.get_num_connections() < 1:
            pass

        rospy.loginfo("/odom subscriber created.")


    # Server callback
    def goal_callback(self, goal):
        rate = rospy.Rate(1)
        dist = 0  # Travelled distance
        success = True
        i = 0

        vec_result_x = []
        vec_result_y = []
        vec_result_z = []

        while dist <= self._dist_one_lap:
            # Check if the goal is cancelled
            if self._as.is_preempt_requested():
                success = False
                self._as.set_preempted()
                break
            
            # Saving odometry readins
            vec_result_x.append(self.position_x)
            vec_result_y.append(self.position_y)
            vec_result_z.append(self.orientation_theta)

            # Travelled distance
            dist += sqrt( pow( vec_result_x[i] - vec_result_x[i-1], 2) + pow( vec_result_y[i] - vec_result_y[i-1], 2) ) 

            self._feedback.current_total = dist
            self._as.publish_feedback(self._feedback)
            # loop variables
            i += 1
            rate.sleep()

        if success:
            print(vec_result_x)
            self._result.list_of_odoms.x = vec_result_x
            self._result.list_of_odoms.y = vec_result_y
            self._result.list_of_odoms.z = vec_result_z
            self._as.set_succeeded(self._result.result.list_of_odoms)
            rospy.loginfo("Finishing the action server.")


    # Odometry callback
    def odom_callback(self, msg):
        self.position_x = msg.pose.pose.position.x
        self.position_y = msg.pose.pose.position.y
        self.orientation_theta = msg.pose.pose.orientation.z

if __name__ == '__main__':
    rospy.init_node("record_odometry_server_node")
    RecordOdometry()
    rospy.spin()