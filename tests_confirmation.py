import threading
import time
import keyboard
from robot_module import robot_singleton

if __name__ == "__main__":
    robot = robot_singleton()
    robot.connect()
    robot.open_tool()
    input('Press Enter to start to close gripper')
    robot.close_tool()
    position = robot.get_joint_angles()
    thread = threading.Thread(target=robot.confirmation())
    thread.start()
    while keyboard.is_pressed('space'):
        robot.move_joints((0, 0, 0, 0, 0, 0))
        robot.move_joints(position)
    print(robot.have_medicine)
    robot.stop_confirmation()






