#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import time


class SerialBridgeNode(Node):
    def __init__(self):
        super().__init__('serial_bridge')
        self.subscription = self.create_subscription(
            String,
            '/robot_command',
            self.cmd_callback,
            10
        )

        self.port = '/dev/ttyACM0'
        self.baud = 115200
        self.ser = None

        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=1)
            time.sleep(2)
            self.get_logger().info(f'Connected to Serial Port: {self.port}')
        except Exception as e:
            self.get_logger().error(f'Failed to open serial port {self.port}: {e}')

    def cmd_callback(self, msg):
        if self.ser and self.ser.is_open:
            data_to_send = f"{msg.data}\n"
            self.ser.write(data_to_send.encode('utf-8'))

    def destroy_node(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = SerialBridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
