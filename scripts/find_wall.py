#! /usr/bin/env python

import rospy
import time
from section2.srv import FindWall, FindWallResponse
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def callback(msg):
    global data
    data = msg

def my_callback(request):
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    sub = rospy.Subscriber('/scan', LaserScan, callback)
    move = Twist()
    rate = rospy.Rate(1)
    rate.sleep() #rospy.spin()  mantain the service open.
    rospy.loginfo("The Service FindWall has been called")
    global data
    move = Twist()
    turn = 0
    X_Speed = 0.1
    x = 80
    t = 80
    out = 0
    
    while not rospy.is_shutdown() and out == 0: 
         # values at 0 degree
         #print ("Right ", data.ranges[0])
         # values at 90 degree
         #print ("Middle ",data.ranges[360])
         # values at 180 degree
         #print ("Left ", data.ranges[719])
         scan_right = data.ranges[0]  
         scan_middle = data.ranges[360] 
         scan_left = data.ranges[719] 

         if scan_middle  < 0.2 and turn == 0: 
                     turn = 0
                     move.linear.x = -0.0 #Move the robot with a linear velocity in the x axis
                     move.angular.z = 0.0 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(x)
                     #print ('Backward0')
         elif scan_middle == float('inf') and turn == 1:
                turn = 0
                if scan_right >= 0.3: #and scan_left == float('inf'):
                     turn = 0
                     out = 1
                     move.angular.z = 0.0 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(x)
                     #print ('Turn0')
                elif scan_right >= 0.3: #and scan_left >= 0.2:
                     turn = 0
                     out = 1
                     move.angular.z = 0.0 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(x)
                     #print ('Turn0')                
         elif scan_middle >= 0.7 and turn == 1:          
                if scan_right >= 0.3: #and scan_left == float('inf'):
                     turn = 0
                     out = 1
                     move.angular.z = 0.0 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(x)
                     #print ('Turn0')
                elif scan_right >= 0.3: #and scan_left >= 0.2:
                     turn = 0
                     out = 1
                     move.angular.z = 0.0 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(x)
                     #print ('Turn0') 

         elif scan_middle == float('inf') and turn == 0:  
                turn = 0
                if scan_right == float('inf') and scan_left == float('inf'):
                     move.linear.x = X_Speed #Move the robot with a linear velocity in the x axis
                     move.angular.z = 0.0 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(x)
                     #print ('Forward0')
                     turn = 0
                elif scan_right > 0.3 and scan_right > 0.3:
                     move.linear.x = X_Speed #Move the robot with a linear velocity in the x axis
                     move.angular.z = 0.0 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(x)
                     #print ('Forward0')
                elif scan_right > 0.3 and scan_right < 0.5:
                     move.linear.x = X_Speed #Move the robot with a linear velocity in the x axis
                     move.angular.z = -0.4 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(x)
                     #print ('Forward and turn right0')
                     turn = 0
                elif scan_right < 0.6: #and scan_left >= 0.3:
                     move.linear.x = 0.0 #Move the robot with a linear velocity in the x axis
                     move.angular.z = 0.4 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(x)
                     #print ('Forward and turn left0')
                     turn = 0
                elif scan_right == float('inf') and scan_left <= 0.3:
                     move.linear.x = 0.0 #Move the robot with a linear velocity in the x axis
                     move.angular.z = -0.4 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(x)
                     #print ('Forward and turn right0')
                     turn = 0
         elif scan_middle > 0.7 and turn == 0: 
                turn = 0
                if scan_right == float('inf') and scan_left == float('inf'):
                     move.linear.x = X_Speed #Move the robot with a linear velocity in the x axis
                     move.angular.z = 0.0 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(x)
                     #print ('Forward0')
                     turn = 0
                elif scan_right >= 0. and scan_right >= 0.5:
                     move.linear.x = X_Speed #Move the robot with a linear velocity in the x axis
                     move.angular.z = 0.0 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(x)
                     #print ('Forward0')
                     turn = 0
                elif scan_right > 0.3 and scan_right < 0.5:
                     move.linear.x = X_Speed #Move the robot with a linear velocity in the x axis
                     move.angular.z = -0.4 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(x)
                     #print ('Forward and turn right0')
                     turn = 0
                elif scan_right < 0.6: #and scan_left >= 0.3:
                     move.linear.x = 0.0 #Move the robot with a linear velocity in the x axis
                     move.angular.z = 0.4 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(x)
                     #print ('Forward and turn left0')
                     turn = 0
                elif scan_right == float('inf') and scan_left <= 0.3:
                     move.linear.x = 0.0 #Move the robot with a linear velocity in the x axis
                     move.angular.z = -0.4 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(x)
                     #print ('Forward and turn right0')
                     turn = 0
         elif scan_middle <= 0.7 and scan_middle > 0.2 and turn == 0:
                turn = 1
                if scan_right == float('inf') and scan_left == float('inf'):
                     move.linear.x = 0.0 #Move the robot with a linear velocity in the x axis
                     move.angular.z = 0.5 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(t)
                     #print ('Turn left1')
                     turn = 1
                elif scan_right == float('inf') and scan_left <= 0.3:
                     move.linear.x = 0.0 #Move the robot with a linear velocity in the x axis
                     move.angular.z = 0.5 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(t)
                     #print ('Turn left1')
                     turn = 1
                elif scan_right < 0.2 and scan_left == float('inf'):
                     move.linear.x = 0.0 #Move the robot with a linear velocity in the x axis
                     move.angular.z = 0.5 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(t)
                     #print ('Turn left1')
                     turn = 1
                elif scan_right >= 0.3 and scan_left >= 0.3:
                     move.linear.x = 0.0 #Move the robot with a linear velocity in the x axis
                     move.angular.z = 0.5 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(t)
                     #print ('Turn left1')
                     turn = 1
         elif scan_middle < 0.6 and turn == 1:
                     rate = rospy.Rate(t)
                     #print ('keep Turning1')
                     turn = 1
         else:
                     #print ('Else')
                     move.linear.x = 0.1 #Move the robot with a linear velocity in the x axis
                     #move.angular.z = 0.0 #Move the with an angular velocity in the z axis
                     rate = rospy.Rate(x)
         # publish 
         pub.publish(move) 
         rate.sleep()
         time.sleep(1)        
                     
    rospy.loginfo("Finished service find_wall")
    move.linear.x = 0
    move.angular.z = 0
    pub.publish(move)
    rate = rospy.Rate(1)
    rate.sleep()
    
    response = FindWallResponse()
    response.wallfound = True
    return response # the service Response class, in this case EmptyResponse

def main():
  rospy.init_node('service_Find_Wall') 
  my_service = rospy.Service('/find_wall', FindWall , my_callback) # create the Service called move_bb8_in_square_custom with the defined callback
  rospy.loginfo("Service /find_wall Ready")
  rate = rospy.Rate(1)
  while not rospy.is_shutdown():
       rate.sleep() #rospy.spin()  mantain the service open.
  
main()

if __name__ == '__main__': 
    try: 
        main() 
    except rospy.ROSInterruptException: 
        pass