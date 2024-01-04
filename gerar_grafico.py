from typing import Tuple, List, Dict

import matplotlib.pyplot as plt


def read_archive(name_archive) -> list[str]:
    with open(name_archive, 'r') as archive:
        lines = archive.readlines()
    return lines


def prepossessing_datas(lines) -> tuple[
    list[float], list[float], list[float], list[float], dict[str, int], list[float], list[float]]:
    first_current = []
    second_current = []
    first_positions = []
    second_positions = []
    average = []
    difference = []
    results = {'True': 0, 'False': 0}

    for line in lines:
        if 'True' in line:
            results['True'] += 1
        elif 'False' in line:
            results['False'] += 1
        elif 'First Current' in line:
            first_current.append(float(line.split(':')[-1].strip()))
        elif 'Second Current' in line:
            second_current.append(float(line.split(':')[-1].strip()))
        elif 'First Position' in line:
            first_positions.append(float(line.split(':')[-1].strip()))
        elif 'Second Position' in line:
            second_positions.append(float(line.split(':')[-1].strip()))
        elif 'Average' in line:
            average.append(float(line.split(':')[-1].strip()))
        elif 'Difference' in line:
            difference.append(float(line.split(':')[-1].strip()))

    return first_current, second_current, first_positions, second_positions, results, average, difference


def generate_graph(list_1: list, name_list_1: str, list_2: list, name_list_2: str) -> None:

    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(list_1, color='c')
    plt.title(f'Variation of {name_list_1}')
    plt.xlabel('Rotation')
    plt.ylabel(name_list_1)
    plt.ylim((min(list_1) - 0.8), (max(list_1) + 0.8)) # Get 0.3, 0.8 - Not

    # Gerando gráfico para a variação de Posição
    plt.subplot(1, 2, 2)
    plt.plot(list_2, color='c')
    plt.title(f'Variation of {name_list_2}')
    plt.xlabel('Rotation')
    plt.ylabel(name_list_2)
    plt.ylim((min(list_2)-0.8), max(list_2)+0.8) # Get 91.5, 99.5 - Not

    # Exibindo os gráficos
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    name_archive = 'text_implet_not'

    linhas = read_archive(name_archive)
    first_cu, second_cu, first_po, second_po, results, average, difference = prepossessing_datas(linhas)

    generate_graph(first_cu, "First Current", second_cu, "Second Current")
    generate_graph(first_po, "First Position", second_po, "Second Position")
    generate_graph(average, "Average", difference, "Difference")

    currents = 0
    for e in first_cu:
        currents += e
    print('First Current media: ', currents/len(first_cu))

    posi_amount = 0
    for j in second_cu:
        posi_amount += j
    print('Second Current media: ', posi_amount/len(second_cu))

    currents = 0
    for e in first_po:
        currents += e
    print('First Position media: ', currents/len(first_po))

    posi_amount = 0
    for j in second_po:
        posi_amount += j
    print('Second Position media: ', posi_amount/len(second_po))

    currents = 0
    for e in average:
        currents += e
    print('Average media: ', currents/len(average))

    posi_amount = 0
    for j in difference:
        posi_amount += j
    print('Difference media: ', posi_amount/len(difference))


    print("Resultados:")
    for resultado, valor in results.items():
        print(f"{resultado}: {valor}")
