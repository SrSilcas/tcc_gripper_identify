import threading
import time

import keyboard

from robot_module.robot import robot_singleton, Robot


class ConfirmationTest:

    def __init__(self):
        """
        Initializes the variables necessary
        """
        self.argument = True

    def stop(self):
        """
        Stops the program

        Returns:
            :return None
        """
        while self.argument:
            if keyboard.is_pressed('space'):
                self.argument = False


def movement(robot_: Robot):
    """
    This method create the movement of the robot
    Args:
        :param(Robot) robot_: the robot to move

    Returns:
        :return None
    """
    args = ConfirmationTest()
    stop = threading.Thread(target=args.stop)
    stop.start()
    while robot_.continuous and args.argument:
        if args.argument and robot_.continuous:
            robot_.move_joints((73.450, 327.840, 75.271, 359.842, 300.046, 2.865))
        print(robot_.continuous)
        time.sleep(0.5)
        if args.argument and robot_.continuous:
            robot_.move_joints((0, 0, 0, 0, 0, 0))
        print(robot_.continuous)
        time.sleep(0.5)


if __name__ == "__main__":
    robot = robot_singleton
    robot.connect()
    robot.open_tool(0.65)
    time.sleep(0.5)
    robot.move_joints((73.450, 327.840, 75.271, 359.842, 300.046, 2.865))
    input('Press any key to start')
    print(robot.close_tool(1.80, 1.95))
    movement(robot)
