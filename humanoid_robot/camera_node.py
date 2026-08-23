import cv2
from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image


class CameraPublisher(Node):

  def __init__(self):
    super().__init__('camera_publisher')

    # Topic publisher
    self.publisher_ = self.create_publisher(Image, '/camera/image_raw', 10)

    # Timer (30 FPS -> interval approx 0.033 sec)
    self.timer = self.create_timer(0.033, self.timer_callback)

    # OpenCV Camera Setup (V4L2 + MJPG + 640x480)
    self.cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L2)
    self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    self.cap.set(cv2.CAP_PROP_FPS, 30)

    self.bridge = CvBridge()
    self.get_logger().info('Camera Publisher Node has been started successfully.')

  def timer_callback(self):
    ret, frame = self.cap.read()
    if ret:
      # Convert OpenCV image (BGR) to ROS Image message
      msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
      msg.header.stamp = self.get_clock().now().to_msg()
      msg.header.frame_id = 'camera_frame'

      self.publisher_.publish(msg)

  def destroy_node(self):
    self.cap.release()
    super().destroy_node()


def main(args=None):
  rclpy.init(args=args)
  node = CameraPublisher()
  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    pass
  finally:
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
  main()
