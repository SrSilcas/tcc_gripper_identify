import matplotlib.pyplot as plt


def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    return linhas


def processar_dados(linhas):
    # Inicializando listas para armazenar dados
    bigger = []
    lesser = []
    amount = []

    resultados = {'True': 0, 'False': 0}

    # Processando linhas do arquivo
    for linha in linhas:
        if 'True' in linha:
            resultados['True'] += 1
        elif 'False' in linha:
            resultados['False'] += 1
        elif 'Bigger' in linha:
            bigger.append(float(linha.split(':')[-1].strip()))
        elif 'Lesser' in linha:
            lesser.append(float(linha.split(':')[-1].strip()))
        elif 'Amount' in linha:
            amount.append(float(linha.split(':')[-1].strip()))

    return bigger, lesser, amount, resultados


def gerar_grafico(biggers, lessers, amounts):
    # Gerando gráfico para a variação de Current_motor
    plt.figure(figsize=(20, 10))

    plt.subplot(1, 3, 1)
    plt.plot(biggers, color='c')
    plt.title('biggers')
    plt.xlabel('Rotação')
    plt.ylabel('Current motor')
    plt.ylim(min(biggers), max(biggers))

    # Gerando gráfico para a variação de Posição
    plt.subplot(1, 3, 2)
    plt.plot(lessers, color='c')
    plt.title('lessers')
    plt.xlabel('Rotação')
    plt.ylabel('Current motor')
    plt.ylim(min(lessers), max(lessers))

    # Gerando gráfico para a variação de Posição
    plt.subplot(1, 3, 3)
    plt.plot(amounts, color='c')
    plt.title('amounts')
    plt.xlabel('Rotação')
    plt.ylabel('Current motor')
    plt.ylim(min(amounts), max(amounts))

    # Exibindo os gráficos
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Nome do arquivo a ser lido
    nome_arquivo = 'confirmation_tests_without'

    # Lendo o arquivo e processando os dados
    linhas = ler_arquivo(nome_arquivo)
    bigger, lesser, amount, results = processar_dados(linhas)

    # Gerando gráficos
    gerar_grafico(bigger, lesser, amount)

    print("Resultados:")
    for resultado, valor in results.items():
        print(f"{resultado}: {valor}")

    print("Max and mim Bigger:", max(bigger), min(bigger))
    print("Max and mim Lesser:", max(lesser), min(lesser))
    print("Max and mim Amount:", max(amount), min(amount))
