import matplotlib.pyplot as plt

def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    return linhas

def processar_dados(linhas):
    # Inicializando listas para armazenar dados
    current_motor = []
    posicao = []
    resultados = {'True': 0, 'False': 0}

    # Processando linhas do arquivo
    for linha in linhas:
        if 'True' in linha:
            resultados['True'] += 1
        elif 'False' in linha:
            resultados['False'] += 1
        elif 'Current_mottor' in linha:
            current_motor.append(float(linha.split(':')[-1].strip()))
        elif 'Position' in linha:
            posicao.append(float(linha.split(':')[-1].strip()))

    return current_motor, posicao, resultados

def gerar_grafico(current_motor, posicao):
    # Gerando gráfico para a variação de Current_motor
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(current_motor, color='c')
    plt.title('Variação de Current_motor')
    plt.xlabel('Rotação')
    plt.ylabel('Current_motor')
    plt.ylim(0.2, 0.6) # Get 0.3, 0.8 - Not 

    # Gerando gráfico para a variação de Posição
    plt.subplot(1, 2, 2)
    plt.plot(posicao, color='c')
    plt.title('Variação de Posição')
    plt.xlabel('Rotação')
    plt.ylabel('Posição')
    plt.ylim(94.5, 98.5) # Get 91.5, 99.5 - Not

    # Exibindo os gráficos
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Nome do arquivo a ser lido
    nome_arquivo = 'text_main_implet_1_not.txt'

    # Lendo o arquivo e processando os dados
    linhas = ler_arquivo(nome_arquivo)
    current_motor, posicao, resultados = processar_dados(linhas)

    # Gerando gráficos
    gerar_grafico(current_motor, posicao)
    current = 0
    for e in current_motor:
        current += e
    print('Corrente media: ',current/50)
    posi_amount = 0
    for j in posicao:
        posi_amount += j
    print('Posição media: ',posi_amount/50)
    # Exibindo resultados True/False
    print("Resultados:")
    for resultado, valor in resultados.items():
        print(f"{resultado}: {valor}")

