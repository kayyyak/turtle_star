#!/usr/bin/python3

# from my_controller.dummy_module import dummy_function, dummy_var
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Point
from turtlesim.msg import Pose
# from turtlesim_plus_interfaces.srvs
from std_srvs.srv import Empty
import math
import sys


class DummyNode(Node):
    def __init__(self):
        super().__init__('dummy_node')
        self.pub_cmdvel = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.create_subscription(Point, "/mouse_position", self.mouse_position_callback, 10)
        self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)
        self.create_timer(0.01, self.timer_callback)
        self.target = [0.0, 0.0, 0.0]
        self.current_pose = [0.0, 0.0, 0.0]

    def pose_callback(self, msg):
        self.current_pose[0] = msg.x
        self.current_pose[1] = msg.y
        self.current_pose[2] = msg.theta
        print(self.current_pose) 

    def mouse_position_callback(self, msg):
        self.target[0] = msg.x
        self.target[1] = msg.y
        self.target[2] = msg.z
        print(self.target)

    def cmd_vel(self, vx, w):
        cmd_vel = Twist()
        cmd_vel.linear.x = vx
        cmd_vel.angular.z = w
        self.pub_cmdvel.publish(cmd_vel)

    def timer_callback(self):
        self.cmd_vel(0.1, 0.1)


def main(args=None):
    rclpy.init(args=args)
    node = DummyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
