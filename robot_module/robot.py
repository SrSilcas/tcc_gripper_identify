import threading
import statistics
from time import sleep
import robot_module.utils as robot_connection
from robot_module.size_of_medcines import Utils
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
        self.requisition = None
        self.have_medicine = None
        self.continuous = None
        self.continue_confirmation = None

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

    def __increment(self, have_medicine: bool = False) -> float:
        increment = [1.2, 1.2, 1.2, 1.2]
        position = self.attribute_from_gripper()["position"]

        if have_medicine:
            return (position + increment[3]) / 100
        elif position < 70:
            return (position + increment[2]) / 100
        elif position < 85:
            return (position + increment[1]) / 100
        else:
            return (position + increment[0]) / 100

    def close_tool(self, cap_size:float = 0, body_size:float = 0) -> tuple[bool, float, float, float]:
        """
        This function close the gripper and try detected object

        Args:
            cap_size (float, optional): size for cap of object. Defaults to 0.
            body_size (float, optional): size for body of object. Defaults to 0.

        Returns:
            tuple[bool, float, float, float]: tuple here the first (bool) is whether an object was detected or not detected
            the second (float) when gripper identify the object the third (float) max approach calculate for this object and the 
            fourth (float) min approach calculate for this object
        """

        object_detected = False
        currents = []
        if cap_size != 0 and body_size != 0:
            max_approach = self.__calculate_size(cap_size)
            min_approach = self.__calculate_size(body_size) - 1
        
        position = 0

        while not object_detected and self.attribute_from_gripper()["position"] < max_approach:

            deviation = None
            average = None
            self.__close()
            first_current = self.attribute_from_gripper()["current_motor"]

            if 4 > first_current > 0:
                if len(currents) > 3:
                    deviation = statistics.stdev(currents)
                    average = statistics.mean(currents)
            else:
                print("atypical current")

            if deviation is not None and self.attribute_from_gripper()['position'] > min_approach:
                if self.__verification(first_current, deviation, average):
                    position = self.attribute_from_gripper()['position']
                    self.__close()
                    second_current = self.attribute_from_gripper()["current_motor"]
                    object_detected = self.__verification(second_current, deviation, average)
                    if object_detected:
                        self.__close()
                        # thread = threading.Thread(target=self.confirmation)
                        # thread.start()
                        self.final_position = self.attribute_from_gripper()["position"] / 100

            if 4 > first_current > 0 and len(currents) < 7:
                currents.append(first_current)

        return object_detected, position, max_approach, min_approach

    def __close(self, have_medicine_: bool = False):
        """
        This Function close the gripper

        Args:
            have_medicine_ (bool, optional): Already medicine inside the gripper. Defaults to False.
        """
        gripper_command = Base_pb2.GripperCommand()
        finger = gripper_command.gripper.finger.add()
        gripper_command.mode = Base_pb2.GRIPPER_POSITION
        finger.finger_identifier = 1
        finger.value = self.__increment(have_medicine=have_medicine_)
        self.base.SendGripperCommand(gripper_command)

    def confirmation(self):
        """
        This function check if medicine continuos into gripper, in a thread and change the robot attribute 

        """
        self.continuous = True
        currents = []
        self.continue_confirmation = True

        while self.continue_confirmation and self.continuous:
            current = self.attribute_from_gripper()['current_motor']

            if 2 < current > 0 and len(currents) > 15:
                deviation = statistics.stdev(currents)
                average = statistics.mean(currents)

                if not self.__verification_confirmation(current, deviation, average):
                    count = 0
                    continuous = False

                    while count < 10 and not continuous:
                        current = self.attribute_from_gripper()['current_motor']
                        if self.__verification_confirmation(current, deviation, average):
                            continuous = True
                        count += 1

                    if count > 9 and not continuous:
                        self.continuous = False

            if len(currents) < 15:
                currents.append(current)

    def stop_confirmation(self):
        """
        When this function is called the confirmation is stopped 

        """
        self.continue_confirmation = False

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

    @staticmethod
    def __calculate_size(size:float)-> float:
        """
        This function calculate with size of object the quantity

        Args:
            size (float): size of object in cm

        Returns:
            float: quantity for gripper
        """
        size_ = Utils.calculate_approach(size)
        return size_

    @staticmethod
    def __verification(current: float, deviation: float, average_:float) -> bool:
        """
        This function analyse currents for identify if have medicine into gripper

        Args:
            current (float): current for analyse
            deviation (float): deviation for list of currents
            average_ (float): average for the list of currents

        Returns:
            bool: this current confirm if have medicine or not
        """
        return_ = False
        if (deviation * 0.35) <= current - average_ and current > 0.6:
            return_ = True

        return return_

    @staticmethod
    def __verification_confirmation(current: float, deviation: float, average_) -> bool:
        """
        This function analyse currents for identify if have medicine into gripper

        Args:
            current (float): current for analyse
            deviation (float): deviation for list of currents
            average_ (float): average for the list of currents

        Returns:
            bool: this current confirm if have medicine or not
        """
        return_ = True
        if (deviation * 0.6) <= average_ - current:
            return_ = False

        return return_

    def attribute_from_gripper(self)-> dict:
        """
        This function to manage information's from base cyclic about gripper

        Returns:
           dict: all information's into dict for access with keys position, velocity and current_motor
        """
        variable = self.base_cyclic.RefreshFeedback().__str__().split()
        position = variable.index("gripper_feedback")
        information_gripper = {"position": float(variable[position + 7]),
                               "velocity": float(variable[position + 9]),
                               "current_motor": float(variable[position + 11])}

        return information_gripper
    
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

    def get_pose_cartesian(self):
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

    def apply_emergency_stop(self):
        self.base.ApplyEmergencyStop()

    @staticmethod
    def get_gripper_command():
        return Base_pb2.GripperCommand()



"""
Here we create a singleton instance of RobotExecutionContext for use
in robot_provider and robot_controller.
"""
robot_singleton = Robot()
