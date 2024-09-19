import matplotlib.pyplot as plt


def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    return linhas


def processar_dados(linhas_):
    final_positions = []
    positions = []
    deviations = []
    averages = []
    first_currents = []
    second_currents = []

    resultados = {'True': 0, 'False': 0}

    for linha_ in linhas_:
        if 'temperature' in linha_:
            temperature.append(float(linha_.split(':')[-1].strip()))
        elif 'velocity' in linha_:
            velocity.append(float(linha_.split(':')[-1].strip()))
        elif 'position' in linha_:
            position.append(float(linha_.split(':')[-1].strip()))
        elif 'current_motor' in linha_:
            current.append(float(linha_.split(':')[-1].strip()))

    return temperature, velocity, position, current


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
    nome_arquivo = 'close_gripper.txt'

    # Lendo o arquivo e processando os dados
    linhas_argv = ler_arquivo(nome_arquivo)
    temperature, velocity, position, current = processar_dados(linhas_argv)

    # Gerando gráficos
    gerar_grafico(temperature, velocity, ('temperature', 'velocity'))
    gerar_grafico(position, current, ('position', 'current'))

