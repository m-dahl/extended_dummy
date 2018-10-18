# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
import math
from std_msgs.msg import String
from unification_msgs.msg import State, Control

from sys import argv

def main(args=None):
    topic = 'extended_dummy'
    if len(argv) > 1: topic = topic+argv[1]
    state_topic = topic+'/state'
    control_topic = topic+'/control'

    rclpy.init(args=args)

    node = rclpy.create_node('extended_dummy')
    publisher = node.create_publisher(State, state_topic)

    active = False
    ref_pos = 0
    act_pos = 0
    has_tool = False

    idle_counter = 0

    def timer_callback():
        nonlocal act_pos, ref_pos, active, has_tool, idle_counter
        if active and ref_pos != act_pos:
            diff = ref_pos-act_pos
            act_pos = act_pos + int(math.copysign(1, diff))

        # build new state
        msg = State()
        msg.act_pos = act_pos
        msg.has_tool = has_tool
        msg.ack_ref_pos = ref_pos
        msg.ack_active = active

        idle_counter+=1
        if (idle_counter > 25):
            node.get_logger().info('Idle, resetting to intial state')
            act_pos = 0
            ref_pos = 0
            active = False
            has_tool = False
        else:
            node.get_logger().info('Publishing: "%s"' % msg)
            publisher.publish(msg)


    timer_period = 0.2  # seconds
    timer = node.create_timer(timer_period, timer_callback)

    def control_callback(msg):
        nonlocal active, ref_pos, idle_counter
        active = msg.active
        ref_pos = msg.ref_pos
        node.get_logger().info('I heard: "%s"' % msg)
        idle_counter = 0

    subscription = node.create_subscription(Control, control_topic, control_callback)
    # subscription  # prevent unused variable warning

    rclpy.spin(node)

    # Destroy the timer attached to the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_timer(timer)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
