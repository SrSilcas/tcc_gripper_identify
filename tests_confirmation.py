import threading
import time
import keyboard
from robot_module import robot_singleton

if __name__ == "__main__":
    robot = robot_singleton
    robot.connect()
    robot.open_tool()
    input('Press Enter to start to close gripper')
    robot.close_tool()
    position = (359.9981689453125, 343.920, 75.13192749023438, 359.9029541015625, 300.0187683105469, 359.9910888671875)
    thread = threading.Thread(target=robot.confirmation)
    thread.start()
    while not keyboard.is_pressed('space'):
        robot.move_joints((0, 0, 0, 0, 0, 0))
        robot.move_joints(position)
    print(robot.have_medicine)
    robot.stop_confirmation()
    print(thread.is_alive())






