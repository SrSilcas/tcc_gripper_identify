from robot_module import robot_singleton
from time import sleep


if __name__ == '__main__':

    true = 0
    false = 0
    robot = robot_singleton
    robot.connect()
    robot.open_tool(0.65)
    sleep(0.5)

    for i in range(10):
        print(robot.close_tool())
        input('Case the medicine is into gripper')
        for j in range(10):
            response = robot.is_holding()

            if response[0]:
                true += 1

            else:
                false += 1

            print(response)

        robot.open_tool(0.65)
        input('Put the medicine into gripper')

    print(f'True holdings: {true}')
    print(f'False holdings: {false}')
