import time
from robot_module.robot import robot_singleton


if __name__ == "__main__":
    robot = robot_singleton
    robot.connect()
    true = 0
    false = 0
    for i in range(50):
        robot.open_tool(0.65)
        time.sleep(1)
        response = robot.close_tool(0.8)
        if response[0]:
            true += 1
        else:
            false += 1
        print(response)
        time.sleep(1)

    robot.open_tool(0.65)
    print(f'True response: {true}')
    print(f'False response: {false}')
    # for i in range(5):
    #     print(robot.is_holding())
    #     time.sleep(2)
