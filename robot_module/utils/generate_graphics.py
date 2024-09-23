import matplotlib.pyplot as plt


def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    return linhas


def processar_dados(linhas_):
    final_position = []
    position_ = []
    deviation = []
    average = []
    first = []
    second = []

    resultados = {'True': 0, 'False': 0}

    for linha in linhas_:
        if 'True' in linha:
            resultados['True'] += 1
        elif 'False' in linha:
            resultados['False'] += 1
        elif 'Final' in linha:
            try:
                final_position.append(float(linha.split(' ')[-1].strip()))
            except ValueError as e:
                print(e)
        elif 'Position' in linha:
            position_.append(float(linha.split(' ')[-1].strip()))
        elif 'Deviation' in linha:
            deviation.append(float(linha.split(' ')[-1].strip()))
        elif 'Average' in linha:
            average.append(float(linha.split(' ')[-1].strip()))
        elif 'First' in linha:
            first.append(float(linha.split(' ')[-1].strip()))
        elif 'Second' in linha:
            second.append(float(linha.split(' ')[-1].strip()))

    return final_position, position_, deviation, average, first, second, resultados


def gerar_grafico(information_1, information_2, names_information: tuple):
    # Gerando gráfico para a variação de Current_motor
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(information_1, color='c')
    plt.title(f'{names_information[0]}')
    plt.xlabel('Rotação')
    plt.ylabel('value')
    plt.ylim(min(information_1) - 0.05, max(information_1) + 0.05)

    # Gerando gráfico para a variação de Posição
    plt.subplot(1, 2, 2)
    plt.plot(information_2, color='c')
    plt.title(f'{names_information[1]}')
    plt.xlabel('Rotação')
    plt.ylabel('value')
    plt.ylim(min(information_2) - 0.05, max(information_2) + 0.05)

    # Exibindo os gráficos
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Nome do arquivo a ser lido
    nome_arquivo = 'close_gripper_no_med_23_09.txt'

    # Lendo o arquivo e processando os dados
    linhas_argv = ler_arquivo(nome_arquivo)
    final_position, position_, deviation, average, first, second, results = processar_dados(linhas_argv)

    # Gerando gráficos
    gerar_grafico(final_position, position_, ('final_position', 'position_'))
    gerar_grafico(deviation, average, ('deviation', 'average'))
    gerar_grafico(first, second, ('first', 'second'))
    print(results)

