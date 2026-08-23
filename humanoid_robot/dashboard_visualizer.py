import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point

class DashboardVisualizer(Node):
    def __init__(self):
        super().__init__('dashboard_visualizer')
        self.marker_pub = self.create_publisher(Marker, '/visual_markers', 10)
        self.timer = self.create_timer(0.2, self.publish_markers)

    def publish_markers(self):
        # 1. Red 3D Ball
        ball = Marker()
        ball.header.frame_id = "base_link"
        ball.header.stamp = self.get_clock().now().to_msg()
        ball.ns = "ball"
        ball.id = 0
        ball.type = Marker.SPHERE
        ball.action = Marker.ADD
        ball.pose.position.x = 0.6
        ball.pose.position.y = 0.0
        ball.pose.position.z = -0.1
        ball.scale.x = 0.12
        ball.scale.y = 0.12
        ball.scale.z = 0.12
        ball.color.r = 1.0
        ball.color.g = 0.0
        ball.color.b = 0.0
        ball.color.a = 1.0

        # 2. Green Straight Path Line
        line = Marker()
        line.header.frame_id = "base_link"
        line.header.stamp = self.get_clock().now().to_msg()
        line.ns = "path"
        line.id = 1
        line.type = Marker.LINE_STRIP
        line.action = Marker.ADD
        line.scale.x = 0.02
        line.color.r = 0.0
        line.color.g = 1.0
        line.color.b = 0.0
        line.color.a = 1.0

        p1 = Point(x=0.0, y=0.0, z=-0.1)
        p2 = Point(x=0.6, y=0.0, z=-0.1)
        line.points = [p1, p2]

        self.marker_pub.publish(ball)
        self.marker_pub.publish(line)

def main():
    rclpy.init()
    node = DashboardVisualizer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
