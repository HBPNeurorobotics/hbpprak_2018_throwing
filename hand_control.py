# Only 8 joints are actuated, the rest are passive
# values taken from the urdf model at http://wiki.ros.org/schunk_svh_driver
RANGE_MAX = {
    "Index": {"Index_Proximal": 0.79849, "Index_Medial": 1.334},
    "Middle": {"Middle_Proximal": 0.79849, "Middle_Medial": 1.334},
    "Ring": {"Ring_Proximal": 0.98175},
    "Pinky": {"Pinky_Proximal": 0.98175},
    "Thumb": {"Thumb_Opposition": 0.9879, "Thumb_Flexion": 0.9704}
}
# grasping factors for the cylinder
GRASPING_FACTORS = {
    "Index": {"Index_Proximal": 0.3, "Index_Medial": 0.3},
    "Middle": {"Middle_Proximal": 0.3, "Middle_Medial": 0.3},
    "Ring": {"Ring_Proximal": 0.3},
    "Pinky": {"Pinky_Proximal": 0.3},
    "Thumb": {"Thumb_Opposition": 0.8, "Thumb_Flexion": 0.2}
}

@nrp.MapVariable("RANGE_MAX", initial_value=RANGE_MAX)
@nrp.MapVariable("GRASPING_FACTORS", initial_value=GRASPING_FACTORS)
@nrp.MapVariable("Index_Proximal", initial_value=0.0)
@nrp.MapVariable("Index_Medial", initial_value=0.0)
@nrp.MapVariable("Middle_Proximal", initial_value=0.0)
@nrp.MapVariable("Middle_Medial", initial_value=0.0)
@nrp.MapVariable("Ring_Proximal", initial_value=0.0)
@nrp.MapVariable("Pinky_Proximal", initial_value=0.0)
@nrp.MapVariable("Thumb_Flexion", initial_value=0.0)
@nrp.MapVariable("Thumb_Opposition", initial_value=0.0)
@nrp.MapRobotPublisher("topic_Index_Proximal", Topic('/robot/hand_Index_Finger_Proximal/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_Index_Medial", Topic('/robot/hand_Index_Finger_Distal/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_index_distal", Topic('/robot/hand_j14/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_Middle_Proximal", Topic('/robot/hand_Middle_Finger_Proximal/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_Middle_Medial", Topic('/robot/hand_Middle_Finger_Distal/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_middle_distal", Topic('/robot/hand_j15/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_Ring_Proximal", Topic('/robot/hand_Ring_Finger/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_ring_medial", Topic('/robot/hand_j12/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_ring_distal", Topic('/robot/hand_j16/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_Pinky_Proximal", Topic('/robot/hand_Pinky/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_pinky_medial", Topic('/robot/hand_j13/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_pinky_distal", Topic('/robot/hand_j17/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_Thumb_Opposition", Topic('/robot/hand_Thumb_Opposition/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_Thumb_Flexion", Topic('/robot/hand_Thumb_Flexion/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_thumb_medial", Topic('/robot/hand_j3/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_thumb_distal", Topic('/robot/hand_j4/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_palm", Topic('/robot/hand_j5/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotSubscriber('command', Topic('/arm_robot/hand_commands', std_msgs.msg.String))
@nrp.MapVariable("last_command_executed", initial_value=None)
@nrp.Neuron2Robot()
def hand_control(t, command, last_command_executed,
                    RANGE_MAX, GRASPING_FACTORS,
                    Index_Proximal, topic_Index_Proximal,
                    Index_Medial, topic_Index_Medial,
                    topic_index_distal,
                    Middle_Proximal, topic_Middle_Proximal,
                    Middle_Medial, topic_Middle_Medial,
                    topic_middle_distal,
                    Ring_Proximal, topic_Ring_Proximal,
                    topic_ring_medial,
                    topic_ring_distal,
                    Pinky_Proximal, topic_Pinky_Proximal,
                    topic_pinky_medial,
                    topic_pinky_distal,
                    Thumb_Flexion, topic_Thumb_Flexion,
                    topic_thumb_distal,
                    topic_thumb_medial,
                    Thumb_Opposition, topic_Thumb_Opposition,
                    topic_palm):

    if command.value is None:
        return
    else:
        command_str = command.value.data

    if command_str == last_command_executed.value:
        return

    clientLogger.info("HAND received: {}".format(command_str))

    # Index
    def flex_index(RANGE_MAX, FACTORS, grasp):
        Index_Proximal.value = RANGE_MAX["Index_Proximal"] * FACTORS["Index_Proximal"] * grasp
        topic_Index_Proximal.send_message(std_msgs.msg.Float64(Index_Proximal.value))
        Index_Medial.value = RANGE_MAX["Index_Medial"] * FACTORS["Index_Medial"] * grasp
        topic_Index_Medial.send_message(std_msgs.msg.Float64(Index_Medial.value))
        # distal joint mimics Medial with a 1.045 coefficient
        topic_index_distal.send_message(std_msgs.msg.Float64(Index_Medial.value * 1.045))

    # Middle
    def flex_middle(RANGE_MAX, FACTORS, grasp):
        Middle_Proximal.value = RANGE_MAX["Middle_Proximal"] * FACTORS["Middle_Proximal"] * grasp
        topic_Middle_Proximal.send_message(std_msgs.msg.Float64(Middle_Proximal.value))
        Middle_Medial.value = RANGE_MAX["Middle_Medial"] * FACTORS["Middle_Medial"] * grasp
        topic_Middle_Medial.send_message(std_msgs.msg.Float64(Middle_Medial.value))
        middle_distal = Middle_Medial.value * 1.0434
        topic_middle_distal.send_message(std_msgs.msg.Float64(middle_distal))

    # Ring
    def flex_ring(RANGE_MAX, FACTORS, grasp):
        Ring_Proximal.value = RANGE_MAX["Ring_Proximal"] * FACTORS["Ring_Proximal"] * grasp
        topic_Ring_Proximal.send_message(std_msgs.msg.Float64(Ring_Proximal.value))
        ring_medial = Ring_Proximal.value * 1.3588
        topic_ring_medial.send_message(std_msgs.msg.Float64(ring_medial))
        ring_distal = Ring_Proximal.value * 1.42307
        topic_ring_distal.send_message(std_msgs.msg.Float64(ring_distal))

    # Pinky
    def flex_pinky(RANGE_MAX, FACTORS, grasp):
        Pinky_Proximal.value = RANGE_MAX["Pinky_Proximal"] * FACTORS["Pinky_Proximal"] * grasp
        topic_Pinky_Proximal.send_message(std_msgs.msg.Float64(Pinky_Proximal.value))
        pinky_medial = Pinky_Proximal.value * 1.35880
        topic_pinky_medial.send_message(std_msgs.msg.Float64(pinky_medial))
        pinky_distal = Pinky_Proximal.value * 1.42307
        topic_pinky_distal.send_message(std_msgs.msg.Float64(pinky_distal))

    # Thumb
    def flex_thumb(RANGE_MAX, FACTORS, grasp):
        Thumb_Opposition.value = RANGE_MAX["Thumb_Opposition"] * FACTORS["Thumb_Opposition"] * grasp
        topic_Thumb_Opposition.send_message(std_msgs.msg.Float64(Thumb_Opposition.value))
        Thumb_Flexion.value = RANGE_MAX["Thumb_Flexion"] * FACTORS["Thumb_Flexion"] * grasp
        topic_Thumb_Flexion.send_message(std_msgs.msg.Float64(Thumb_Flexion.value))
        thumb_distal = Thumb_Flexion.value * 1.44889
        topic_thumb_distal.send_message(std_msgs.msg.Float64(thumb_distal))
        thumb_medial = Thumb_Flexion.value * 1.01511
        topic_thumb_medial.send_message(std_msgs.msg.Float64(thumb_medial))
        # Palm
        topic_palm.send_message(std_msgs.msg.Float64(Thumb_Opposition.value * 0.3))

    do_flex = {
        "Index": flex_index,
        "Middle": flex_middle,
        "Ring": flex_ring,
        "Pinky": flex_pinky,
        "Thumb": flex_thumb
    }

    def parse_grasping_command(cmd):
        do_grasp = None
        if cmd == "GRASP":
            do_grasp = 1
        elif cmd == "RELEASE":
            do_grasp = 0
        return do_grasp

    grasp = parse_grasping_command(command_str)
    if grasp is not None:
        last_command_executed.value = command_str
        for finger_name in do_flex.keys():
            do_flex[finger_name](RANGE_MAX.value[finger_name], GRASPING_FACTORS.value[finger_name], grasp)
