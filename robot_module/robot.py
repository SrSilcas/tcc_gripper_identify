import statistics
import threading
from time import sleep

from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from kortex_api.autogen.client_stubs.BaseCyclicClientRpc import BaseCyclicClient
from kortex_api.autogen.client_stubs.GripperCyclicClientRpc import GripperCyclicClient
from kortex_api.autogen.messages import Base_pb2

import robot_module.utils as robot_connection
from robot_module.size_of_medcines import SizeOfMedicines

TIMEOUT_DURATION = 20


class Robot:
    def __init__(self, gripper_test=False) -> None:
        """
        Method to initialize the robot class generate the necessary parameters for the operation

        Returns:
            :return None
        """
        self.action = None
        self.arm_state_notif_handle = None
        self.base = None
        self.base_cyclic = None
        self.device = None
        self.error = None
        self.gripper = None
        self.router = None
        self.gripper_command = None
        self.final_position = None
        self.have_medicine = None
        self.continuous = None
        self.continue_confirmation = None
        self.limit = False
        self.currents = []
        self.gripper_test = gripper_test

    @staticmethod
    def check_for_end_or_abort(e) -> any:
        """
        Return a closure checking for END or ABORT notifications

        Args:
            :param(any) e: event to signal when the action is completed
            (will be set when an END or ABORT occurs)

        Returns:
            :return(any): a closure checking for END or ABORT
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
            :param(list) joints_list: lista with values for all joints for movement

        Returns:
            :return(bool) move is finished
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
            :param(float) pose[0]: x value
            :param(float) pose[1]: y value
            :param(float) pose[2]: z value
            :param(float) 180 - abs(pose[3]): theta_x value
            :param(float) -pose[4]: theta_y value
            :param(float) 180 + pose[5]: theta_z value

        Returns:
            :return(bool): Move is finished
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
            :param(Any) obj_notification: Instructions for movement or joints or cartesian

        Returns:
            :return(bool): Move is finished
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
        except Exception as e:
            raise e

        finished = e.wait(TIMEOUT_DURATION)

        self.base.Unsubscribe(notification_handle)

        return finished

    def __increment(self, have_medicine: bool = False) -> float:
        """
        This "private" function is only use to pass to function __close diferentes displacement quotients to gripper
        close slowly

        Args:
            :param(bool) have_medicine:

        Returns:
            (float) the new value of the displacement quotient for close to gripper
        """
        increment = [1.6, 8]
        position = self.attribute_from_gripper()["position"]

        if have_medicine:
            position = (position + increment[1]) / 100
        else:
            position = (position + increment[0]) / 100

        if position > 1:
            return 1

        return position

    def close_tool(self):
        """
        This function close the gripper and try detected object

        Returns:
            a bool argument whether an object was detected or not detected
        """
        if self.gripper_test:
            return True

        self.final_position = None
        self.have_medicine = False
        self.currents = []
        first_current = second_current = 0
        position = 0

        while not self.have_medicine and self.attribute_from_gripper()["position"] < 95:

            self.__close()
            first_current = self.attribute_from_gripper()["current_motor"]
            position = self.attribute_from_gripper()["position"]

            if 4 > first_current > 0:

                if len(self.currents) > 3:

                    if self.__verification(first_current) and first_current > 0.46:

                        self.final_position = self.attribute_from_gripper()['position'] / 100
                        self.__close()

                        second_current = self.attribute_from_gripper()['current_motor']

                        if self.__verification(second_current) and second_current > 0.55:
                            self.have_medicine = True

            else:
                print("atypical current")

            self.__is_valid_current(first_current)

        deviation = statistics.stdev(self.currents)
        average = statistics.mean(self.currents)

        return self.have_medicine, self.final_position, position, deviation, average, first_current, second_current

    def is_holding(self):
        """
        Method to check if gripper is holding an object or not using the list of currents from gripper

        Returns:
            A bool argument whether gripper is holding or not
        """
        count_overall = 0
        count = 0
        current = 0

        if self.have_medicine:
            self.open_tool()
            while count < 2 and count_overall < 5:

                if self.final_position:
                    self.open_tool(self.final_position)

                self.__close(True)
                current = self.attribute_from_gripper()["current_motor"]

                if self.__verification_confirmation(current):
                    self.have_medicine = True
                    if self.final_position:
                        self.open_tool(self.final_position)
                    return self.have_medicine, self.currents, current

                if current > 0.009:
                    count += 1

                count_overall += 1

        self.have_medicine = False
        return self.have_medicine, self.currents, current

    def __close(self, have_medicine_: bool = False) -> None:
        """
        This "private" method is the basic gripper movement function using diferentes displacement quotients originating
        to __increment

        Args:
            have_medicine_: indicative for the __increment that the object has already been detected

        Returns:

        """
        gripper_command = Base_pb2.GripperCommand()
        finger = gripper_command.gripper.finger.add()
        gripper_command.mode = Base_pb2.GRIPPER_POSITION
        finger.finger_identifier = 1
        finger.value = self.__increment(have_medicine=have_medicine_)
        self.base.SendGripperCommand(gripper_command)

    def open_tool(self, value=0.60) -> None:
        """
        Open griper with value
        Args
            :param(float) value: Value for open grips

        Returns:
            :return None
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

    @staticmethod
    def __calculate_size(size: float) -> float:
        """
        This function calculate with size of object the quantity

        Args:
            size: size of object in cm

        Returns:
            Quantity for gripper close in percentage
        """
        size_ = SizeOfMedicines.calculate_approach(size)
        return size_

    def __verification(self, current: float) -> bool:
        """
        This "private" method receives the current of the last movement and the standard deviation and average of the
        last movements and checks if the current has varied enough to infer that the object was detected

        Args:
            current: current for analyse

        Returns:
            True if the current has varied enough to infer that the object was detected
        """
        deviation = statistics.stdev(self.currents)
        average = statistics.mean(self.currents)

        return_ = False

        if deviation <= current - average and self.attribute_from_gripper()['position'] < 96:
            return_ = True

        return return_

    def __is_valid_current(self, current: float):
        """
        This "private" method checks if the current is valid if was that current is appended into the list currents

        Args:
            current: value current to analyses

        Returns:

        """
        average = 0

        if len(self.currents) >= 2:
            average = statistics.mean(self.currents)

        if 4 > current > 0 and len(self.currents) < 7 and current > average * 0.7:
            self.currents.append(current)

    def __verification_confirmation(self, current: float) -> bool:
        """
        This "private" method receives the last current and the standard deviation and average from the last currents
        and checks if the current has varied enough to infer that the object missing

        Args:
            current: the current value to analysis

        Returns:
            True if the current has varied enough to infer that the object was continuous into the gripper
        """
        deviation = statistics.stdev(self.currents)
        average = statistics.mean(self.currents)
        return_ = False
        if deviation <= current - average:
            return_ = True

        return return_

    def attribute_from_gripper(self) -> dict:
        """
        This function to manage information's from base cyclic about gripper

        Returns:
           a dict contains all gripper information's for access with keys position, velocity, current_motor and
           temperature
        """
        variable = self.base_cyclic.RefreshFeedback().interconnect.gripper_feedback.motor[0]
        information_gripper = {"position": variable.position,
                               "velocity": variable.velocity,
                               "current_motor": variable.current_motor,
                               "temperature": variable.temperature_motor}

        return information_gripper
    
    def connect(self, connection_ip: str = "192.168.2.10") -> None:
        """
        Connect api with the robot,
        using the ethernet connection ip as default connection

        Returns:
            :return None
        """
        self.device = robot_connection.RobotConnection.create_tcp_connection(connection_ip)
        self.router = self.device.connect()
        self.base = BaseClient(self.router)
        self.base_cyclic = BaseCyclicClient(self.router)
        self.gripper = GripperCyclicClient(self.router)
        # self.open_tool()

    def disconnect(self):
        """
        Finish connection with robot

        Returns:
            :return None
        """
        if not self.device:
            return
        self.device.disconnect()
        self.base = None
        self.base_cyclic = None
        self.device = None
        self.router = None

    def get_joint_angles(self) -> list[any]:
        """
        Get joint angles from robot.

        Returns:
            :return(list): joint_angles: list with all joints angles
        """
        joint_angles_obj = self.base.GetMeasuredJointAngles()
        joint_angles_list = joint_angles_obj.joint_angles
        joint_angles = []
        for joint in joint_angles_list:
            joint_angles.append(joint.value)

        return joint_angles

    def get_pose_cartesian(self) -> list[any]:
        """
        Get actual cartesian pose from robot.

        Returns:
            :return(list): final_pose: list with cartesian pose
        """
        joint_cartesian_pose = self.base.GetMeasuredCartesianPose()

        joint_poses = [
            joint_cartesian_pose.x,
            joint_cartesian_pose.y,
            joint_cartesian_pose.z,
            joint_cartesian_pose.theta_x,
            joint_cartesian_pose.theta_y,
            joint_cartesian_pose.theta_z
        ]

        return joint_poses

    def apply_emergency_stop(self) -> None:
        """
        This function applies emergency stop with API

        Returns:
            None
        """
        self.base.ApplyEmergencyStop()


"""
Here we create a singleton instance of RobotExecutionContext for use
in robot_provider and robot_controller.
"""
robot_singleton = Robot()
