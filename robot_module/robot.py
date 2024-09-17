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
        self.current = 0
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
            :return(float) the new value of the displacement quotient for close to gripper
        """
        increment = [1.4, 1.6]
        position = self.attribute_from_gripper()["position"]

        if have_medicine:
            return (position + increment[1]) / 100
        else:
            return (position + increment[0]) / 100

    def close_tool(self, cap_size):
        """

        :param cap_size:
        :return:
        """
        self.final_position = self.__calculate_size(cap_size) / 100
        self.have_medicine = False
        self.currents = []

        self.limit = False

        thread = threading.Thread(target=self.verification_gripper)
        thread.start()

        self.open_tool(0.97)

        while not self.have_medicine and not self.limit:
            if self.limit or self.have_medicine:
                break

        position = self.attribute_from_gripper()['position']
        return self.have_medicine, self.final_position, position, self.currents, self.current

    def verification_gripper(self):
        """

        Returns:

        """
        limit = (self.final_position * 100) + 0.5

        if limit > 94:
            limit = 94

        while not self.limit and not self.have_medicine:

            if self.attribute_from_gripper()['position'] > limit:
                self.limit = True
                break

            deviation = None
            average = None
            self.current = self.attribute_from_gripper()['current_motor']

            if 4 > self.current > 0:

                if len(self.currents) >= 2:
                    deviation = statistics.stdev(self.currents)
                    average = statistics.mean(self.currents)

                if deviation is not None and self.current > 0.5:
                    response = self.__verification(self.current, deviation, average)
                    if response:
                        self.have_medicine = True

            else:
                print('Atypical current')

            if 4 > self.current > 0 and len(self.currents) < 4 and not self.have_medicine:
                self.currents.append(self.current)

    def is_holding(self):
        """

        Returns:

        """
        self.current = 0

        if self.have_medicine:
            for i in range(2):
                self.__close()

                self.current = self.attribute_from_gripper()["current_motor"]

                response = self.attribute_from_gripper()['position'] / 100

                while response < self.final_position:
                    response = self.attribute_from_gripper()['position'] / 100

                if len(self.currents) >= 2:
                    deve = statistics.stdev(self.currents)
                    mean = statistics.mean(self.currents)

                    if self.__verification_confirmation(self.current, deve, mean):
                        self.have_medicine = True
                        return self.have_medicine, self.currents, self.current

                self.open_tool(self.final_position)

        self.have_medicine = False
        return self.have_medicine, self.currents, self.current

    def __close(self) -> None:
        """
        This Function close the gripper

        Args:
            :param(bool, optional) have_medicine_: Already medicine inside the gripper. Defaults to False.

        Returns:
            :return None
        """
        gripper_command = Base_pb2.GripperCommand()
        finger = gripper_command.gripper.finger.add()
        gripper_command.mode = Base_pb2.GRIPPER_POSITION
        finger.finger_identifier = 1
        finger.value = self.__increment(have_medicine=True)
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
            :param(float) size: size of object in cm

        Returns:
            :return(float): quantity for gripper
        """
        size_ = SizeOfMedicines.calculate_approach(size)
        return size_

    @staticmethod
    def __verification(current: float, deviation: float, average_: float) -> bool:
        """
        This "private" method receives the current of the last movement and the standard deviation and average of the
        last movements and checks if the current has varied enough to infer that the object was detected

        Args:
            :param(float) current: current for analyse
            :param(float) deviation: the standard deviation of the last movements
            :param(float) average_: average for the list of currents

        Returns:
            :return(bool): True if the current has varied enough to infer that the object was detected
        """
        return_ = False
        if deviation <= current - average_:
            return_ = True

        return return_

    @staticmethod
    def __verification_confirmation(current: float, deviation: float, average_) -> bool:
        """
        This "private" method receives the last current and the standard deviation and average from the last currents
        and checks if the current has varied enough to infer that the object missing

        Args:
            :param current(float): the current value to analysis
            :param deviation(float): the standard deviation of the last movements
            :param average_(float): average value of the last movements

        Returns:
            :return(bool): True if the current has varied enough to infer that the object was missing
        """
        print(f'Deviation: {deviation}')
        print(f'Current: {current}')
        print(f'Average: {average_}')
        return_ = False
        if deviation * 0.5 <= current - average_:
            return_ = True

        return return_

    def attribute_from_gripper(self) -> dict:
        """
        This function to manage information's from base cyclic about gripper

        Returns:
           :return(dict): all information's into dict for access with keys position, velocity and current_motor
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
