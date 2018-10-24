# Imported Python Transfer Function
@nrp.MapRobotPublisher('arm_1', Topic('/robot/arm_1_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher('arm_2', Topic('/robot/arm_2_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher('arm_3', Topic('/robot/arm_3_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher('arm_4', Topic('/robot/arm_4_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher('arm_5', Topic('/robot/arm_5_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher('arm_6', Topic('/robot/arm_6_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_index_proximal", Topic('/robot/hand_Index_Finger_Proximal/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_index_distal", Topic('/robot/hand_Index_Finger_Distal/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_middle_proximal", Topic('/robot/hand_Middle_Finger_Proximal/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_middle_distal", Topic('/robot/hand_Middle_Finger_Distal/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_ring_proximal", Topic('/robot/hand_Ring_Finger/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_ring_distal", Topic('/robot/hand_j12/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_pinky_proximal", Topic('/robot/hand_Pinky/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_pinky_distal", Topic('/robot/hand_j13/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_thumb_flexion", Topic('/robot/hand_j4/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("hand_thumb_distal", Topic('/robot/hand_j3/cmd_pos', std_msgs.msg.Float64))
@nrp.Neuron2Robot()
def simple_move_robot(t,
                     hand_index_proximal,
                     hand_index_distal,
                     hand_middle_proximal,
                     hand_middle_distal,
                     hand_ring_proximal,
                     hand_ring_distal,
                     hand_pinky_proximal,
                     hand_pinky_distal,
                     hand_thumb_flexion,
                     hand_thumb_distal,
                     arm_1,
                     arm_2,
                     arm_3,
                     arm_4 ,
                     arm_5,
                     arm_6):
    import numpy as np
    def grasp(strength):
        for topic in [
                hand_index_proximal,
                hand_index_distal,
                hand_middle_proximal,
                hand_middle_distal,
                hand_ring_proximal,
                hand_ring_distal,
                hand_pinky_proximal,
                hand_pinky_distal,
                hand_thumb_flexion,
                hand_thumb_distal
        ]:
            topic.send_message(std_msgs.msg.Float64(strength))

    arm_1.send_message(std_msgs.msg.Float64(-0.6))
    arm_2.send_message(std_msgs.msg.Float64(np.sin(t)))
    arm_3.send_message(std_msgs.msg.Float64(-np.sin(t)))
    arm_4.send_message(std_msgs.msg.Float64(0.5))
    arm_5.send_message(std_msgs.msg.Float64(0.5))
    arm_6.send_message(std_msgs.msg.Float64(0.5))
    grasp(-np.sin(t))
