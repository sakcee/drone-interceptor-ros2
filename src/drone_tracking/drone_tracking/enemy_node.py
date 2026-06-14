import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class EnemyNode(Node):
    def __init__(self):
        super().__init__('enemy_node')
        self.cmd_vel_pub = self.create_publisher(Twist, '/enemy/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.move_circle)
        self.angle = 0.0

    def move_circle(self):
        twist = Twist()
        self.angle += 0.05
        # Quadcopter ko circle me ghumane ke liye velocity math
        twist.linear.x = 1.0 * math.cos(self.angle)
        twist.linear.y = 1.0 * math.sin(self.angle)
        self.cmd_vel_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = EnemyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()