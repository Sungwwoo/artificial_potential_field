# 1#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Pose, PoseStamped, Transform, TransformStamped, Vector3, Quaternion
from std_msgs.msg import String, Header
from actionlib_msgs.msg import GoalStatusArray
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from tf import TransformBroadcaster


sendTransform = False
goal_trans = Vector3()
goal_rot = Quaternion()


def cbMoveBaseGoal(goal):
    global sendTransform
    global goal_trans
    global goal_rot

    goal_trans.x = goal.pose.position.x
    goal_trans.y = goal.pose.position.y
    goal_trans.z = goal.pose.position.z

    goal_rot = goal.pose.orientation

    sendTransform = True
    rospy.loginfo("Constructing TF at [" + str(goal_trans.x) + ", " + str(goal_trans.y) + "]")


if __name__ == "__main__":
    rospy.init_node("goal_tf_constructor", disable_signals=True)

    sendTransform = False
    goal_trans = Vector3()
    goal_rot = Quaternion()
    br = TransformBroadcaster()
    sub_base_goal = rospy.Subscriber("/move_base/current_goal", PoseStamped, cbMoveBaseGoal, queue_size=2)

    while not rospy.is_shutdown():
        if sendTransform:
            trans = Transform(translation=goal_trans, rotation=goal_rot)
            header = Header()
            header.stamp = rospy.Time.now()
            header.frame_id = "map"
            trans_stamped = TransformStamped(header, "goal", trans)
            br.sendTransformMessage(trans_stamped)
            # For testing potential calculation
            rospy.sleep(1)
