import matplotlib.pyplot as plt


def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    return linhas


def processar_dados(linhas):
    # Inicializando listas para armazenar dados
    current = []
    initial_currents = []

    resultados = {'True': 0, 'False': 0}

    # Processando linhas do arquivo
    for linha in linhas:
        if 'True' in linha:
            resultados['True'] += 1
        elif 'False' in linha:
            resultados['False'] += 1
        elif 'Current' in linha:
            current.append(float(linha.split(':')[-1].strip()))
        elif 'Initial' in linha:
            initial_currents.append(float(linha.split(':')[-1].strip()))

    return current, initial_currents, resultados


def gerar_grafico(currents, inital_current):
    # Gerando gráfico para a variação de Current_motor
    plt.figure(figsize=(10, 20))

    plt.subplot(1, 2, 1)
    plt.plot(currents, color='c')
    plt.title('Variação de Current_motor')
    plt.xlabel('Rotação')
    plt.ylabel('Current_motor')
    plt.ylim(min(currents), max(currents))

    # Gerando gráfico para a variação de Posição
    plt.subplot(1, 2, 2)
    plt.plot(inital_current, color='c')
    plt.title('Variação de Posição')
    plt.xlabel('Rotação')
    plt.ylabel('Posição')
    plt.ylim(min(inital_current), max(inital_current))

    # Exibindo os gráficos
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Nome do arquivo a ser lido
    nome_arquivo = 'confirmation_tests'

    # Lendo o arquivo e processando os dados
    linhas = ler_arquivo(nome_arquivo)
    current, inital, resultados = processar_dados(linhas)

    # Gerando gráficos
    gerar_grafico(current, inital)

    print("Resultados:")
    for resultado, valor in resultados.items():
        print(f"{resultado}: {valor}")

