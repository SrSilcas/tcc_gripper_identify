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
    tuple_current = []
    list_position_diff = []
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
        tuple_current.append(return_[1])
        list_position_diff.append(return_[2])

        result = f'Rotation: {i}\n  Response: {return_[0]}\n  Current: {return_[1]}\n  Position Diff: {return_[2]}\n'

        results += result
    robot_singleton.open_tool()

    write_into_txt(results, 'confirmation_get')

    generate_graphic(tuple_current, 'Current', list_position_diff, 'Position')

    print("Confirmou ", confirmou)
    print("Não Confirmou ", nao_confirmou)
