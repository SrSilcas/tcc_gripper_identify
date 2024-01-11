import time
import matplotlib.pyplot as plt
from robot_module import robot_singleton
from robot_module import write_into_txt


def generate_graph(list_1: list, name_list_1: str, list_2: list, name_list_2: str) -> None:
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(list_1, color='c')
    plt.title(f'Variation of {name_list_1}')
    plt.xlabel('Rotation')
    plt.ylabel(name_list_1)
    plt.ylim((min(list_1) - 0.05), (max(list_1) + 0.05))  # Get 0.3, 0.8 - Not

    # Gerando gráfico para a variação de Posição
    plt.subplot(1, 2, 2)
    plt.plot(list_2, color='c')
    plt.title(f'Variation of {name_list_2}')
    plt.xlabel('Rotation')
    plt.ylabel(name_list_2)
    plt.ylim((min(list_2) - 0.05), max(list_2) + 0.05)  # Get 91.5, 99.5 - Not

    # Exibindo os gráficos
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':

    robot_singleton.connect()
    pegou = 0
    nao_pegou = 0
    results = f""
    first_current_list = []
    second_current_list = []
    first_position_list = []
    second_position_list = []
    second_difference_list = []
    first_difference_list = []

    for i in range(1, 51):
        list_ = robot_singleton.new_close_tool()
        time.sleep(0.3)
        pegou_ = list_[0]
        first_current = list_[3]
        second_current = list_[4]
        first_position = list_[1]
        second_position = list_[2]
        second_difference = list_[5]
        first_difference = list_[6]

        first_current_list.append(first_current)
        second_current_list.append(second_current)
        first_position_list.append(first_position)
        second_position_list.append(second_position)
        first_difference_list.append(first_difference)
        second_difference_list.append(second_difference)

        print(pegou_)
        robot_singleton.open_tool(0.7)
        time.sleep(0.3)

        if pegou_:
            pegou += 1
        else:
            nao_pegou += 1
        result = (f"Rotation: {i}\n     {pegou_}\n     First Current: {first_current}\n"
                  f"     Second Current: {second_current}\n     Second Difference: {second_difference}\n"
                  f"     First Difference: {first_difference}\n     First position: {first_position}\n"
                  f"     Second Position: {second_position}\n")
        results += result
        print(i)

    write_into_txt(results, "text_implet_get_hypocaina")
    generate_graph(first_current_list, 'First Current', second_current_list, 'Second Current')
    generate_graph(first_position_list, 'First Position', second_position_list, 'Second Position')
    generate_graph(first_difference_list, 'First Current Difference',
                   second_difference_list, 'Second Current Difference')

    print("Não pegou ", nao_pegou)
    print("Pegou ", pegou)
