#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import SetEntityState
import time
import sys

class RobustInterceptionSystem(Node):
    def __init__(self):
        super().__init__('interceptor_node')
        
        # Creating client connection to the Gazebo simulation pose controller
        self.state_client = self.create_client(SetEntityState, '/set_entity_state')
        
        self.get_logger().info("⏳ Waiting for Gazebo Simulator Service (/set_entity_state)...")
        while not self.state_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("...Still checking for service active state...")

        # Perfect Inline tracking on X-axis (y=0.0 is fixed)
        self.alpha_x = 0.0
        self.enemy_x = 15.0  
        self.flight_altitude = 4.0
        self.is_active = True

        # Running tracking at smooth constant pacing frames
        self.timer = self.create_timer(0.04, self.engagement_loop)
        self.get_logger().info("🎬 SYSTEM READY: Tracking Target within Simulation Frame.")

    def update_model_state(self, name, x, y, z, roll=0.0):
        req = SetEntityState.Request()
        req.state.name = name
        req.state.pose.position.x = float(x)
        req.state.pose.position.y = float(y)
        req.state.pose.position.z = float(z)
        
        # Tracking orientation roll alignment triggers for tumbling effect
        if roll > 0:
            req.state.pose.orientation.x = roll
            req.state.pose.orientation.w = 0.707
        else:
            req.state.pose.orientation.w = 1.0

        self.state_client.call_async(req)

    def engagement_loop(self):
        if not self.is_active:
            return

        distance = self.enemy_x - self.alpha_x

        # Lock interception limits range
        if distance > 2.5:
            self.get_logger().info(f"📡 RADAR LOCK: Closing Range -> {distance:.2f}m")
            
            # Smooth tracking frames moving cleanly forward on Y=0 track plane
            self.enemy_x += 0.4 * 0.04  
            self.update_model_state('enemy_drone', self.enemy_x, 0.0, self.flight_altitude)

            self.alpha_x += 1.4 * 0.04  
            self.update_model_state('delta_interceptor', self.alpha_x, 0.0, self.flight_altitude)
        else:
            self.get_logger().error("⚡ TARGET IN KILL ZONE! FIRING LASER CANNON!")
            self.is_active = False
            self.execute_kill_strike()

    def execute_kill_strike(self):
        self.get_logger().warn("🔴 LASER BEAM ENGAGED!")
        
        # Projects perfectly straight from Interceptor to pierce the enemy model
        laser_spawn_x = self.alpha_x + 40.0
        
        # Fire the ultra-visible red tracking laser beam inline
        self.update_model_state('laser_beam', laser_spawn_x, 0.0, self.flight_altitude)
        
        # Keep interceptor rock solid floating proudly in space
        self.update_model_state('delta_interceptor', self.alpha_x, 0.0, self.flight_altitude)
        
        # Hold display for 4 full seconds for evaluation review
        time.sleep(4.0)

        # Teleport laser away instantly
        self.update_model_state('laser_beam', 0.0, 0.0, -100.0)

        self.get_logger().fatal("💥 TARGET DESTROYED: Enemy drone spinning down!")
        
        # KINETIC CRASH SEQUENCE: Drops ONLY the enemy drone model
        for crash_step in range(30):
            drop_alt = self.flight_altitude - (crash_step * 0.15)
            current_roll = crash_step * 0.4
            
            # Falling down with rotational damage roll loop control
            self.update_model_state(
                'enemy_drone', 
                self.enemy_x + (crash_step * 0.02), 
                0.0, 
                max(0.1, drop_alt), 
                roll=current_roll
            )
            time.sleep(0.06)

        self.destroy_timer(self.timer)
        sys.exit(0)

def main(args=None):
    rclpy.init(args=args)
    node = RobustInterceptionSystem()
    try:
        rclpy.spin(node)
    except SystemExit:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()