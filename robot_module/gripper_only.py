from robot_module.robot import robot_singleton
from kortex_api.autogen.messages import Base_pb2


def close_detection() -> bool:
    """
    This function close the gripper and try detected object
    Returns:
    (bool): object_detect: returns whether an object was detected or not detected
    """
    object_detected = False

    while not object_detected and float(robot_singleton.atribue_from_gripper()["position"]) < 94:
        gripper_command = Base_pb2.GripperCommand()
        finger = gripper_command.gripper.finger.add()
        gripper_command.mode = Base_pb2.GRIPPER_POSITION
        finger.finger_identifier = 1
        finger.value = (float(robot_singleton.atribue_from_gripper()["position"]) + 2) / 100
        robot_singleton.base.SendGripperCommand(gripper_command)

        current = float(robot_singleton.atribue_from_gripper()["current_motor"])
        if 4 < current:
            print("atypical current 1")
            print(current)
            current = 0

        if current > 0.60:
            finger.value = (float(robot_singleton.atribue_from_gripper()["position"]) + 1.15) / 100
            robot_singleton.base.SendGripperCommand(gripper_command)
            current = float(robot_singleton.atribue_from_gripper()["current_motor"])
            if current > 0.40:
                object_detected = True
                print("Object detect")

    return object_detected


def close_destruction():
    """
    This function close the gripper to max
    """
    list_currents = []
    while float(robot_singleton.atribue_from_gripper()["position"]) > 99.9:
        gripper_command = Base_pb2.GripperCommand()
        finger = gripper_command.gripper.finger.add()
        gripper_command.mode = Base_pb2.GRIPPER_POSITION
        finger.finger_identifier = 1
        finger.value = (float(robot_singleton.atribue_from_gripper()["position"]) + 2) / 100
        robot_singleton.base.SendGripperCommand(gripper_command)
        current = robot_singleton.atribue_from_gripper()["current_motor"]
        if current > 0.60:
            position = robot_singleton.atribue_from_gripper()["position"]
            list_currents.append((current, position))
            print("current_motor ----", current)

    return list_currents

