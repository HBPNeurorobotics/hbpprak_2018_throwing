import numpy as np

# APPROACH
approach_red_conf = np.array([0.56958, -0.9, 1.1781, -0.0345, -0.6, 0.0])
# GRASP
grasp_red_conf = np.array([0.5178, -0.9, 1.1781, -0.0345, -0.6, 0.0])
grasp_blue_conf = np.array([-0.5178, -0.9, 1.1781, -0.0345, -0.6, 0.0])
# DISPOSE
dispose_red_conf = np.array([1.3980, -0.9, 1.1781, -0.0345, -0.6, 0.0])
dispose_blue_conf = np.array([0.88026, -0.9, 1.1781, -0.0345, -0.9, 0.0])
# RESET
reset_conf = np.zeros(6)

@nrp.MapRobotPublisher("topic_arm_1", Topic('/robot/arm_1_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_arm_2", Topic('/robot/arm_2_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_arm_3", Topic('/robot/arm_3_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_arm_4", Topic('/robot/arm_4_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_arm_5", Topic('/robot/arm_5_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic_arm_6", Topic('/robot/arm_6_joint/cmd_pos', std_msgs.msg.Float64))
@nrp.MapRobotSubscriber('command', Topic('/arm_robot/arm_commands', std_msgs.msg.String))
@nrp.MapVariable("last_command_executed", initial_value=None)
@nrp.MapVariable("approach_red_conf", initial_value=approach_red_conf)
@nrp.MapVariable("grasp_red_conf", initial_value=grasp_red_conf)
@nrp.MapVariable("grasp_blue_conf", initial_value=grasp_blue_conf)
@nrp.MapVariable("dispose_red_conf", initial_value=dispose_red_conf)
@nrp.MapVariable("dispose_blue_conf", initial_value=dispose_blue_conf)
@nrp.MapVariable("reset_conf", initial_value=reset_conf)
@nrp.Neuron2Robot()
def arm_control(t,
                command, last_command_executed,
                approach_red_conf,
                grasp_red_conf, grasp_blue_conf,
                dispose_red_conf, dispose_blue_conf,
                reset_conf,
                topic_arm_1, topic_arm_2,
                topic_arm_3, topic_arm_4,
                topic_arm_5, topic_arm_6):

    def send_joint_config(topics_list, config_list):
        for topic, value in zip(topics_list, config_list):
            topic.send_message(std_msgs.msg.Float64(value))

    import collections

    if command.value is None:
        return
    else:
        command_str = command.value.data

    if command_str == last_command_executed.value:
        return

    clientLogger.info("ARM received: {}".format(command_str))
    topics_arm = [topic_arm_1, topic_arm_2, topic_arm_3, topic_arm_4, topic_arm_5, topic_arm_6]

    commands_confs = collections.defaultdict(None, {
            "APPROACH": {"RED": approach_red_conf.value},
            "GRASP": {"BLUE": grasp_blue_conf.value, "RED": grasp_red_conf.value},
            "DISPOSE": {"BLUE": dispose_blue_conf.value, "RED": dispose_red_conf.value},
            "RESET": reset_conf.value
        }
    )

    # parse command
    split_command = command_str.split('_')
    action = split_command[0]

    if len(split_command) > 1:
        color = split_command[-1]
        new_config = commands_confs[action][color]
    else:
        new_config = commands_confs[action]
    if new_config is not None:
        last_command_executed.value = command_str
        send_joint_config(topics_arm, new_config)
