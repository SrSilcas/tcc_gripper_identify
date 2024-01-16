import threading
from time import sleep
from typing import Tuple, Union, Any

import robot_module.utils as robot_connection
from kortex_api.autogen.messages import Base_pb2
from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from kortex_api.autogen.client_stubs.BaseCyclicClientRpc import BaseCyclicClient
from kortex_api.autogen.client_stubs.GripperCyclicClientRpc import GripperCyclicClient

TIMEOUT_DURATION = 20


class Robot:
    def __init__(self):
        self.active_state = None
        self.action = None
        self.arm_state_notif_handle = None
        self.base = None
        self.base_cyclic = None
        self.device = None
        self.error = None
        self.gripper = None
        self.router = None
        self.safety_state_notif_handle = None
        self.safety_status = None
        self.gripper_command = None
        self.action_list = []
        self.status_message = []
        self.final_position = None

    @staticmethod
    def check_for_end_or_abort(e):
        """
        Return a closure checking for END or ABORT notifications

        Args:
            (any) e: event to signal when the action is completed
            (will be set when an END or ABORT occurs)
        """

        def check(notification, event=e):
            if notification.action_event == Base_pb2.ACTION_ABORT:
                event.set()

                if notification.abort_details == Base_pb2.ROBOT_IN_FAULT:
                    event.set()

            if notification.action_event == Base_pb2.ACTION_END:
                event.set()

        return check

    def move_joints(self, joints_list):
        """
        Set movement for robot with joints values
        Args:
            (list) joints_list: lista with values for all joints for movement

        Returns:
            (bool) move is finished
        """
        self.action = Base_pb2.Action()
        self.action.name = "Example angular action movement"
        self.action.application_data = ""

        # Place arm straight up
        for joint_id in range(len(joints_list)):
            joint_angle = self.action.reach_joint_angles.joint_angles.joint_angles.add()
            joint_angle.joint_identifier = joint_id
            joint_angle.value = joints_list[joint_id]

        finished = self.__detection_move(Base_pb2)

        if self.arm_state_notif_handle is not None:
            self.base.Unsubscribe(self.arm_state_notif_handle)

        return finished

    def move_cartesian(self, coordinates):
        """
        Set movement for robot with cartesian coordinates
        Args:
            (float) pose[0]: x value
            (float) pose[1]: y value
            (float) pose[2]: z value
            (float) 180 - abs(pose[3]): theta_x value
            (float) -pose[4]: theta_y value
            (float) 180 + pose[5]: theta_z value

        Returns:
            (bool): Move is finished
        """
        self.action = Base_pb2.Action()
        self.action.name = "Example Cartesian action movement"
        self.action.application_data = ""

        cartesian_pose = self.action.reach_pose.target_pose
        cartesian_pose.x = coordinates[0]  # [meters]
        cartesian_pose.y = coordinates[1]  # [meters]
        cartesian_pose.z = coordinates[2]  # [meters]
        cartesian_pose.theta_x = coordinates[3]  # [degrees]
        cartesian_pose.theta_y = coordinates[4]  # [degrees]
        cartesian_pose.theta_z = coordinates[5]  # [degrees]

        e = threading.Event()
        notification_handle = self.base.OnNotificationActionTopic(
            self.check_for_end_or_abort(e),
            Base_pb2.NotificationOptions()
        )

        print("Executing action")
        self.base.ExecuteAction(self.action)

        print("Waiting for movement to finish ...")
        finished = e.wait(TIMEOUT_DURATION)
        self.base.Unsubscribe(notification_handle)

        if finished:
            print("Cartesian movement completed")
        else:
            print("Timeout on action notification wait")
        return finished

    def __detection_move(self, obj_notification: object = None):
        """
        Create a thread and finish robot move
        Args:
            :(Any) action: Instructions for movement or joints or cartesian

        :return:
        (bool): Move is finished
        """

        e = threading.Event()

        if obj_notification == Base_pb2:
            notification_handle = \
                self.base.OnNotificationActionTopic(
                    self.check_for_end_or_abort(e),
                    Base_pb2.NotificationOptions()
                )

        try:
            self.base.ExecuteAction(self.action)
        except (Exception,):
            pass

        finished = e.wait(TIMEOUT_DURATION)

        self.base.Unsubscribe(notification_handle)

        return finished

    def __increment(self, another_way: bool = False) -> float:
        increment = (1.3, 1.5, 2, 1.7)
        position = float(self.attribute_from_gripper()["position"])
        if another_way:
            return (position + increment[3]) / 100
        elif position < 70:
            return (position + increment[2]) / 100
        elif position < 85:
            return (position + increment[1]) / 100
        else:
            return (position + increment[0]) / 100

    def close_tool(self) -> bool:
        """
        This function close the gripper and try detected object
        Returns:
        (bool): returns whether an object was detected or not detected
        """
        object_detected = False
        loops = 0
        currents = 0
        variation = 0.28
        while not object_detected and float(self.attribute_from_gripper()["position"]) < 92.8:
            average = 0
            gripper_command = Base_pb2.GripperCommand()
            finger = gripper_command.gripper.finger.add()
            gripper_command.mode = Base_pb2.GRIPPER_POSITION
            finger.finger_identifier = 1
            finger.value = self.__increment()
            self.base.SendGripperCommand(gripper_command)

            first_current = float(self.attribute_from_gripper()["current_motor"])
            if 4 > first_current:
                loops += 1
                average = currents / loops
            else:
                print("atypical current")

            if loops > 1 and average is not 0:
                if variation <= first_current - average and first_current > 0.61:
                    finger.value = self.__increment()
                    self.base.SendGripperCommand(gripper_command)
                    second_current = float(self.attribute_from_gripper()["current_motor"])

                    if variation <= second_current - average and second_current > 0.6:
                        object_detected = True
                        finger.value = self.__increment(another_way=True)
                        self.base.SendGripperCommand(gripper_command)
                        self.final_position = float(self.attribute_from_gripper()["position"]) / 100
                currents += first_current
        print(loops)
        return object_detected

    def close_tool_test(self) -> tuple[bool, float, float, float, float, float, float]:
        """
        This function close the gripper and try detected object
        Returns:
        (bool): returns whether an object was detected or not detected
        """
        object_detected = False
        loops = 0
        currents = 0
        variation = 0.28
        position_one = 0
        position_two = 0
        first_current = 0
        second_current = 0
        while not object_detected and float(self.attribute_from_gripper()["position"]) < 92.8:
            average = 0
            gripper_command = Base_pb2.GripperCommand()
            finger = gripper_command.gripper.finger.add()
            gripper_command.mode = Base_pb2.GRIPPER_POSITION
            finger.finger_identifier = 1
            finger.value = self.__increment()
            self.base.SendGripperCommand(gripper_command)

            first_current = float(self.attribute_from_gripper()["current_motor"])
            if 4 > first_current:
                loops += 1
                average = currents / loops
            else:
                print("atypical current")

            if loops > 1 and average is not 0:
                print('First Variation', first_current - average, ' First Current:', first_current)
                if variation <= first_current - average and first_current > 0.6:
                    position_one = float(self.attribute_from_gripper()['position'])
                    finger.value = self.__increment()
                    self.base.SendGripperCommand(gripper_command)
                    second_current = float(self.attribute_from_gripper()["current_motor"])
                    print('Second Variation', second_current - average, ' Second Current:', second_current)

                    if variation <= second_current - average and second_current > 0.61:
                        object_detected = True
                        position_two = float(self.attribute_from_gripper()['position'])
                        finger.value = self.__increment()
                        self.base.SendGripperCommand(gripper_command)
                        self.final_position = float(self.attribute_from_gripper()["position"]) / 100
                currents += first_current
        print(loops)
        return (object_detected, position_one, position_two, first_current, second_current, (second_current - average),
                (first_current - average))

    def close_destruction(self) -> list:
        """
        This function close the gripper to max
        :Returns:
        (list): list of currents and positions
        """
        average = 0
        loops = 1
        currents = 0
        max_variation = 0.27
        gripper_command = Base_pb2.GripperCommand()
        finger = gripper_command.gripper.finger.add()
        gripper_command.mode = Base_pb2.GRIPPER_POSITION
        finger.finger_identifier = 1
        tuple_ = []
        while float(robot_singleton.attribute_from_gripper()["position"]) < 98:
            finger.value = self.__increment()
            self.base.SendGripperCommand(gripper_command)
            current, velocity = (float(self.attribute_from_gripper()["current_motor"]),
                                 float(self.attribute_from_gripper()['velocity']))

            if 4 > current:
                currents += current
                average = currents / loops
                loops += 1
            else:
                print("atypical current")

            if loops > 1:
                if average + max_variation < current:
                    position = float(self.attribute_from_gripper()["position"])
                    tuple_.append((current, position, velocity))

        return tuple_

    def open_tool(self, value=0.60):
        """
        Open griper with value
        Args
            :(float) value: Value for open grips
        """
        # Create the GripperCommand we will send
        self.gripper_command = Base_pb2.GripperCommand()
        finger = self.gripper_command.gripper.finger.add()

        # Close the gripper with position increments
        self.gripper_command.mode = Base_pb2.GRIPPER_POSITION
        finger.finger_identifier = 1
        finger.value = value
        self.base.SendGripperCommand(self.gripper_command)

        sleep(0.16)

    def confirmation_gripper(self) -> tuple[bool, float, Union[float, Any]]:

        if self.final_position is None:
            self.final_position = 0.6
        position_before = float(self.attribute_from_gripper()["position"])
        object_continuous = True
        gripper_command = Base_pb2.GripperCommand()
        finger = gripper_command.gripper.finger.add()
        gripper_command.mode = Base_pb2.GRIPPER_POSITION
        finger.finger_identifier = 1
        finger.value = self.__increment(another_way=True)
        self.base.SendGripperCommand(gripper_command)
        current = float(self.attribute_from_gripper()['current_motor'])
        position_after = float(self.attribute_from_gripper()['position'])

        sleep(0.16)

        position_difference = position_after - position_before

        self.open_tool(self.final_position)

        return object_continuous, current, position_difference

    def connect(self, connection_ip: str = "192.168.2.10"):
        """
        Connect api with the robot,
        using the ethernet connection ip as default connection
        """
        self.device = robot_connection.RobotConnection.create_tcp_connection(connection_ip)
        self.router = self.device.connect()
        self.base = BaseClient(self.router)
        self.base_cyclic = BaseCyclicClient(self.router)
        self.gripper = GripperCyclicClient(self.router)
        self.open_tool()

    def disconnect(self):
        """
        Finish connection with robot
        """
        if not self.device:
            return
        self.device.disconnect()
        self.base = None
        self.base_cyclic = None
        self.device = None
        self.router = None

    def get_joint_angles(self):
        joint_angles_obj = self.base.GetMeasuredJointAngles()
        joint_angles_list = joint_angles_obj.joint_angles
        joint_angles = []
        for joint in joint_angles_list:
            joint_angles.append(joint.value)

        return joint_angles

    def get_pose_cartisians(self):
        joint_cartisians_pose = self.base.GetMeasuredCartesianPose()

        joint_poses = [
            joint_cartisians_pose.x,
            joint_cartisians_pose.y,
            joint_cartisians_pose.z,
            joint_cartisians_pose.theta_x,
            joint_cartisians_pose.theta_y,
            joint_cartisians_pose.theta_z
        ]

        return joint_poses

    def apply_emergency_stop(self):
        self.base.ApplyEmergencyStop()

    @staticmethod
    def get_gripper_command():
        return Base_pb2.GripperCommand()

    def attribute_from_gripper(self):
        variable = self.base_cyclic.RefreshFeedback().__str__().split()
        position = variable.index("gripper_feedback")
        information_gripper = {"position": variable[position + 7],
                               "velocity": variable[position + 9],
                               "current_motor": variable[position + 11]}

        return information_gripper


"""
Here we create a singleton instance of RobotExecutionContext for use
in robot_provider and robot_controller.
"""
robot_singleton = Robot()
