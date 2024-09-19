import time
from robot_module.robot import robot_singleton
import keyboard
from robot_module.write_tests import write_into_txt

if __name__ == "__main__":
    robot = robot_singleton
    robot.connect()

    information = ''

    have_medicine = []
    final_position = []
    position = []
    deviation = []
    average = []
    first_current = []
    second_current = []

    final_current = []
    currents_holding = []

    true_close_tool = 0
    false_close_tool = 0

    true_is_holding = 0
    false_is_holding = 0

    for i in range(50):

        robot.open_tool(0.65)
        time.sleep(1)
        response = robot.close_tool()

        if response[0]:
            true_close_tool += 1

        else:
            false_close_tool += 1

        print(response)
        time.sleep(1)
        # for j in range(2):
        #     response_2 = robot.is_holding()
        #
        #     if response_2[0]:
        #         true_is_holding += 1
        #     else:
        #         false_is_holding += 1
        #
        #     # print(response_2)
        #     time.sleep(1)
        #     final_current.append(response_2[2])
        #     currents_holding.append(response_2[1])

        have_medicine.append(response[0])
        final_position.append(response[1])
        position.append(response[2])
        deviation.append(response[3])
        average.append(response[4])
        first_current.append(response[5])
        second_current.append(response[6])

        if keyboard.is_pressed('space'):
            break

    robot.open_tool(0.65)

    for i in range(len(have_medicine)):
        information += (f'Rotation {i + 1}\n   {have_medicine[i]}\n   Final position {final_position[i]}\n   '
                        f'Position{position[i]}\n   Deviation{deviation[i]}\n   Average {average[i]}\n   '
                        f'First current {first_current[i]}\n   Second current {second_current[i]}\n')

    # for i in range(len(final_current)):
    #     print(f'Rotation: {i}')
    #     print(f'Final Current: {final_current[i]}')
    #     print(f'Currents holding: {currents_holding[i]}')

    write_into_txt(information, 'close_gripper_no_med')

    print(f'True close: {true_close_tool}')
    print(f'False close: {false_close_tool}')
    # print(f'True holding: {true_is_holding}')
    # print(f'False holding: {false_is_holding}')
