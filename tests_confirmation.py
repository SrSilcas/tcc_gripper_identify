from robot_module.robot import robot_singleton
import keyboard
import time


def movement(robot_: robot_singleton):
    while robot_.continuous and not keyboard.is_pressed('space'):
        robot_.move_to((0, 0, 0, 0, 0, 0))
        time.sleep(0.5)
        # TODO end this
        robot_.move_to((1, 1, 1, 1, 1, 1))
        time.sleep(0.5)


if __name__ == "__main__":
    robot = robot_singleton()
    robot.connect()
    robot.close_tool()
    movement(robot)

