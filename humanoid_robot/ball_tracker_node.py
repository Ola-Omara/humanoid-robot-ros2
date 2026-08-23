#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import cv2
import numpy as np


class BallTrackerNode(Node):
    def __init__(self):
        super().__init__('ball_tracker_node')
        self.cmd_pub = self.create_publisher(String, '/robot_command', 10)

        self.FRAME_WIDTH = 640
        self.FRAME_HEIGHT = 480

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.FRAME_HEIGHT)

        self.LOWER = np.array([35, 80, 80])
        self.UPPER = np.array([85, 255, 255])

        self.KICK_DISTANCE = 12.0
        self.MIN_BALL_AREA = 600

        self.STATE_SEARCH = 0
        self.STATE_APPROACH = 1
        self.STATE_KICK = 2

        self.prev_x = None
        self.prev_y = None

        self.timer = self.create_timer(0.033, self.process_frame)
        self.get_logger().info('Ball Tracker Node Started.')

    def estimate_distance(self, radius):
        if radius <= 0:
            return 999.0
        ball_diameter_cm = 9.0
        focal_pixel = 475.0
        return (ball_diameter_cm * focal_pixel) / (radius * 2.0)

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)

        blur = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.LOWER, self.UPPER)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        ball_found = False
        dist = 999.0
        error_x = 0

        if contours:
            c = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(c)

            if area > self.MIN_BALL_AREA:
                (bx, by), radius = cv2.minEnclosingCircle(c)
                bx = int(bx)
                by = int(by)

                if self.prev_x is not None:
                    bx = int((bx + self.prev_x) / 2)
                    by = int((by + self.prev_y) / 2)
                self.prev_x = bx
                self.prev_y = by

                ball_found = True
                dist = self.estimate_distance(radius)
                error_x = bx - (self.FRAME_WIDTH // 2)

                cv2.circle(frame, (bx, by), int(radius), (0, 255, 0), 2)
                cv2.circle(frame, (bx, by), 5, (0, 0, 255), -1)
        else:
            self.prev_x = None
            self.prev_y = None

        kick = 0
        if not ball_found:
            state = self.STATE_SEARCH
            error_x = 0
        elif dist < self.KICK_DISTANCE:
            state = self.STATE_KICK
            kick = 1
        else:
            state = self.STATE_APPROACH

        error_x_clipped = int(np.clip(error_x, -320, 320))

        msg = String()
        msg.data = f"{state},{error_x_clipped},{kick}"
        self.cmd_pub.publish(msg)

        cv2.imshow('Football Robot Tracker', frame)
        cv2.waitKey(1)

    def destroy_node(self):
        self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = BallTrackerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
