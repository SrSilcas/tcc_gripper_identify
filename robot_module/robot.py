import threading
from time import sleep
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

    @staticmethod
    def check_for_end_or_abort(e):
        # TODO identify right error
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

    def move_to_get(self):
        """
        Move robot for home position
        """

        list_joints = (
            44.30694580078125,
            310.5279235839844,
            61.80702209472656,
            337.88427734375,
            47.84202575683594,
            211.01341247558594
        )
        self.move_joints(list_joints)

    def move_to_get_inter(self):
        """
        Move robot for position safe after get medicine position
        """
        cordinates = self.get_pose_cartisians()
        cordinates[-2] += 4
        print(cordinates)
        self.move_cartesian(cordinates)

    def move_to_drop(self):
        """

        Move robot for home position

        """
        list_joints = (0, 0, 0, 0, 0, 0)
        self.move_joints(list_joints)

    def move_to_drop_inter(self):
        """
        Move robot for position safe after get medicine position
        """
        cordinates = self.get_pose_cartisians()
        cordinates[-1] += 4
        print(cordinates)
        self.move_cartesian(cordinates)

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

    def close_tool(self) -> bool:
        """
        This function close the gripper and try detected object
        Returns:
        (bool): returns whether an object was detected or not detected
        """
        object_detected = False

        while not object_detected and float(self.atribue_from_gripper()["position"]) < 97:
            gripper_command = Base_pb2.GripperCommand()
            finger = gripper_command.gripper.finger.add()
            gripper_command.mode = Base_pb2.GRIPPER_POSITION
            finger.finger_identifier = 1
            finger.value = (float(self.atribue_from_gripper()["position"]) + 1.7) / 100
            self.base.SendGripperCommand(gripper_command)

            current = float(self.atribue_from_gripper()["current_motor"])
            if 4 < current:
                print("atypical current 1")
                print(current)
                current = 0

            if current > 0.65:
                finger.value = (float(self.atribue_from_gripper()["position"]) + 1.3) / 100
                self.base.SendGripperCommand(gripper_command)
                current = float(self.atribue_from_gripper()["current_motor"])
                if current > 0.52:
                    finger.value = (float(self.atribue_from_gripper()["position"]) + 1.15) / 100
                    self.base.SendGripperCommand(gripper_command)
                    current = float(self.atribue_from_gripper()["current_motor"])
                    if current > 0.44:
                        object_detected = True
                        return object_detected
                    else:
                        print(f"0.49 > {current}")
                else:
                    print(f"0.52 > {current}")

        return object_detected

    def close_destruction(self) -> list:
        """
        This function close the gripper to max
        :Returns:
        (list): list of currents and positions
        """
        list_currents = []
        while float(robot_singleton.atribue_from_gripper()["position"]) < 98:
            gripper_command = Base_pb2.GripperCommand()
            finger = gripper_command.gripper.finger.add()
            gripper_command.mode = Base_pb2.GRIPPER_POSITION
            finger.finger_identifier = 1
            finger.value = (float(self.atribue_from_gripper()["position"]) + 2) / 100
            self.base.SendGripperCommand(gripper_command)
            current = float(self.atribue_from_gripper()["current_motor"])
            if current > 0.60:
                position = float(self.atribue_from_gripper()["position"])
                list_currents.append((current, position))

        return list_currents

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

        sleep(2)

    def connect(self, connection_ip: str = "192.168.2.10"):
        """
        Connect api with the robot,
        using the ethernet connection ip as default connection
        """
        # Create connection to the device and get the router
        self.device = robot_connection.RobotConnection.create_tcp_connection(connection_ip)
        self.router = self.device.connect()
        # Create required services
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

    def atribue_from_gripper(self):
        variable = self.base_cyclic.RefreshFeedback().__str__().split()
        position = variable.index("gripper_feedback")
        informations_gripper = {"position": variable[position + 7],
                                "velocitxy": variable[position + 9],
                                "current_motor": variable[position + 11]}

        return informations_gripper


"""
Here we create a singleton instance of RobotExecutionContext for use
in robot_provider and robot_controller.
"""
robot_singleton = Robot()
