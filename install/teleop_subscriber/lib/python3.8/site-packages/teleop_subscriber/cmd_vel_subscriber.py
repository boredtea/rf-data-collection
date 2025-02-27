import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from megapi import MegaPi

# Define motor ports
MFR = 2  # Motor Front Right
MBL = 3  # Motor Back Left
MBR = 11 # Motor Back Right
MFL = 10 # Motor Front Left

class CmdVelSubscriber(Node):
    def __init__(self):
        super().__init__('cmd_vel_subscriber')
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.listener_callback,
            10)
        self.subscription  # Prevent unused variable warning
        
        # Initialize MegaPi connection (update port if necessary)
        self.bot = MegaPi()
        self.bot.start('/dev/ttyUSB0')  # Ensure this is the correct port

    def listener_callback(self, msg):
        linear_speed = msg.linear.x * 70  # Convert to motor speed range
        angular_speed = msg.angular.z * 40  # Adjust turning speed

        # Compute motor speeds for differential drive
        left_speed = linear_speed - angular_speed
        right_speed = linear_speed + angular_speed
        

        # Set speeds to front and back wheels
        self.bot.motorRun(MFL, int(left_speed))
        self.bot.motorRun(MBL, int(left_speed))
        self.bot.motorRun(MFR, int(right_speed))
        self.bot.motorRun(MBR, int(right_speed))
        

        self.get_logger().info(f'Linear: {linear_speed}, Angular: {angular_speed}')
        self.get_logger().info(f'Left Motors: {left_speed}, Right Motors: {right_speed}')

def main(args=None):
    rclpy.init(args=args)
    node = CmdVelSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()