import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge
import cv2
import numpy as np

class BallDetector(Node):
    def __init__(self):
        super().__init__('ball_detector')
        self.subscription = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)
        self.publisher_ = self.create_publisher(Point, 'ball_position', 10)
        self.bridge = CvBridge()

        # HSV Range for Green Ball
        self.lower_green = np.array([35, 60, 60])
        self.upper_green = np.array([85, 255, 255])

    def estimate_distance(self, radius):
        if radius <= 0:
            return 999.0
        BALL_DIAMETER_CM = 9.0
        FOCAL_PIXEL = 475.0
        return (BALL_DIAMETER_CM * FOCAL_PIXEL) / (radius * 2.0)

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Binary Mask Generation
        mask = cv2.inRange(hsv, self.lower_green, self.upper_green)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        point_msg = Point()

        if contours:
            c = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(c)

            # Lower threshold (300) to detect partially visible ball at edges
            if area > 300:
                (bx, by), radius = cv2.minEnclosingCircle(c)
                bx, by = int(bx), int(by)
                dist = self.estimate_distance(radius)
                error_x = bx - (frame.shape[1] // 2)

                # Send x = error_x, y = distance
                point_msg.x = float(error_x)
                point_msg.y = float(dist)
                point_msg.z = 0.0
                self.publisher_.publish(point_msg)

                # Draw Visuals
                cv2.circle(frame, (bx, by), int(radius), (0, 255, 0), 2)
                cv2.circle(frame, (bx, by), 5, (0, 0, 255), -1)

                # Status Banner
                state_text = "KICK!" if dist < 12 else "APPROACHING"
                color = (0, 0, 255) if dist < 12 else (0, 255, 0)
                
                cv2.rectangle(frame, (0, 0), (frame.shape[1], 45), (30, 30, 30), -1)
                cv2.putText(frame, f"{state_text} | Dist: {dist:.1f} cm", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                
                self.get_logger().info(f'Detected -> ErrorX: {error_x}, Dist: {dist:.1f}cm')
            else:
                self.send_search_state(point_msg, frame)
        else:
            self.send_search_state(point_msg, frame)

        cv2.imshow("ROS 2 Ball Detector", frame)
        cv2.waitKey(1)

    def send_search_state(self, point_msg, frame):
        point_msg.x = -1.0
        point_msg.y = -1.0
        self.publisher_.publish(point_msg)
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 45), (30, 30, 30), -1)
        cv2.putText(frame, "SEARCHING...", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)

def main(args=None):
    rclpy.init(args=args)
    node = BallDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
