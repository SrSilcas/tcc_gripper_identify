import time
import matplotlib.pyplot as plt
from robot_module import write_into_txt
from robot_module import robot_singleton


def generate_graphic(tuple_1: list, name_tuple1: str, tuple_2: list, name_tuple2: str):
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(tuple_1, color='c')
    plt.title(f'Variação de {name_tuple1}')
    plt.xlabel('Rotação')
    plt.ylabel(name_tuple1)
    plt.ylim(min(tuple_1)-0.08, max(tuple_1)+0.08)

    plt.subplot(1, 2, 2)
    plt.plot(tuple_2, color='c')
    plt.title(f'Variação de {name_tuple2}')
    plt.xlabel('Rotação')
    plt.ylabel(name_tuple2)
    plt.ylim(min(tuple_2)-0.08, max(tuple_2)+0.08)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    robot_singleton.connect()

    confirmou = 0
    nao_confirmou = 0

    results = f""
    robot_singleton.open_tool()

    time.sleep(0.5)

    print(robot_singleton.close_tool_test())
    input("Press any key to start test without or if medicine")

    rotation = 0
    tuple_response = []
    tuple_bigger_current = []
    tuple_bigger_current_2 = []
    tuple_amplitude = []
    tuple_media = []
    list_amount = []
    list_difference_b = []
    for i in range(1, 51):
        return_ = robot_singleton.confirmation_gripper()
        rotation += 1

        print(return_[0])

        if return_[0]:
            confirmou += 1
        else:
            nao_confirmou += 1

        print(i)

        tuple_response.append(return_[0])

        tuple_bigger_current.append(return_[1])
        tuple_bigger_current_2.append(return_[2])

        tuple_amplitude.append(return_[3])
        tuple_media.append(return_[4])

        list_amount.append(return_[5])
        list_difference_b.append(return_[6])

        result = (f'Rotation: {i}\n  Amplitude: {return_[3]}\n  Difference B: {return_[6]}\n  '
                  f'Bigger Current: {return_[1]}\n  Bigger Current 2: {return_[2]}\n  Amount: {return_[5]}\n  '
                  f'Less Current: {return_[4]}\n')

        results += result
    robot_singleton.open_tool()

    write_into_txt(results, 'confirmation_get')

    generate_graphic(tuple_amplitude, 'amplitude', tuple_media, 'Less Current')
    generate_graphic(tuple_bigger_current, 'bigger current', tuple_bigger_current_2, 'bigger current 2')
    generate_graphic(list_amount, 'amount', list_difference_b, 'first_difference B')

    print("Confirmou ", confirmou)
    print("Não Confirmou ", nao_confirmou)
