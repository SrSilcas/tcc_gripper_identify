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
    plt.ylim(min(tuple_1), max(tuple_1))

    plt.subplot(1, 2, 2)
    plt.plot(tuple_2, color='c')
    plt.title(f'Variação de {name_tuple2}')
    plt.xlabel('Rotação')
    plt.ylabel(name_tuple2)
    plt.ylim(min(tuple_2), max(tuple_2))

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    robot_singleton.connect()

    confirmou = 0
    nao_confirmou = 0

    results = f""
    robot_singleton.open_tool()

    time.sleep(0.5)

    print(robot_singleton.close_tool())
    input("Press any key to start test without or if medicine")

    rotation = 0
    tuple_response = []
    tuple_bigger_current = []
    tuple_amount = []
    tuple_velocity = []
    tuple_media = []

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
        tuple_amount.append(return_[2])
        tuple_velocity.append(return_[3])
        tuple_media.append(return_[4])

    robot_singleton.open_tool()

    generate_graphic(tuple_amount, 'amount', tuple_media, 'media')
    generate_graphic(tuple_bigger_current, 'bigger current', tuple_velocity, 'velocity')

    write_into_txt(results, "confirmation_tests_without")


    print("Confirmou ", confirmou)
    print("Não Confirmou ", nao_confirmou)
