import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Função para formatar os valores do eixo y para segundos com unidades adequadas
def segundos_formatter(x, pos):
    if x >= 1:
        return f"{x:.0f} s"
    elif x >= 1e-3:
        return f"{x * 1e3:.0f} ms"
    elif x >= 1e-6:
        return f"{x * 1e6:.0f} µs"
    else:
        return f"{x * 1e9:.0f} ns"

# Dados fornecidos
tempo_exec_python_10_bilhoes = 15.004763  # segundos
tempo_exec_c_10_bilhoes = 0.683478  # segundos
tempo_exec_python_mil = 0.00002 # segundos
tempo_exec_c_mil = 0.000022 #segundos

# Fatores de aumento de desempenho de acordo com a Lei de Moore
lei_de_moore = 2  # Suposição de duplicação a cada 18-24 meses
anos = range(0, 11)  # 0 a 10 anos

# Calculando o tempo de execução para 10 bilhões em Python e C ao longo de 10 anos
tempo_exec_python_10_bilhoes_anos = [tempo_exec_python_10_bilhoes * (lei_de_moore ** ano) for ano in anos]
tempo_exec_python_mil_anos = [tempo_exec_python_mil * (lei_de_moore ** ano) for ano in anos]
tempo_exec_c_mil_anos = [tempo_exec_c_mil * (lei_de_moore ** ano) for ano in anos]
tempo_exec_c_10_bilhoes_anos = [tempo_exec_c_10_bilhoes * (lei_de_moore ** ano) for ano in anos]

# Calculando o tempo em segundos com redução de tempo a cada 2 anos
tempo_exec_python_10_bilhoes_segundos = [tempo_exec_python_10_bilhoes]
tempo_exec_c_10_bilhoes_segundos = [tempo_exec_c_10_bilhoes]
tempo_exec_python_mil_segundos = [tempo_exec_python_mil]
tempo_exec_c_mil_segundos = [tempo_exec_c_mil]

# Variáveis para armazenar as diferenças
linhas_python_10_bilhoes = [1]  # Inicialmente, a linha começa em 1
linhas_c_10_bilhoes = [1]  # Inicialmente, a linha começa em 1
linhas_c_mil = [1]
linhas_python_mil = [1]

# Regras para adicionar novas linhas
for i in range(1, len(anos)):
    tempo_exec_python_10_bilhoes_segundos.append(tempo_exec_python_10_bilhoes_segundos[-1] / 2)
    tempo_exec_c_10_bilhoes_segundos.append(tempo_exec_c_10_bilhoes_segundos[-1] / 2)
    tempo_exec_c_mil_segundos.append(tempo_exec_c_mil_segundos[-1] / 2)
    tempo_exec_python_mil_segundos.append(tempo_exec_python_mil_segundos[-1] / 2)

    diferenca_python_10_bilhoes = tempo_exec_python_10_bilhoes_segundos[i-1] - tempo_exec_python_10_bilhoes_segundos[i]
    diferenca_c_10_bilhoes = tempo_exec_c_10_bilhoes_segundos[i-1] - tempo_exec_c_10_bilhoes_segundos[i]
    diferenca_c_mil = tempo_exec_c_mil_segundos[i-1] - tempo_exec_c_mil_segundos[i]
    diferenca_python_mil = tempo_exec_python_mil_segundos[i-1] - tempo_exec_python_mil_segundos[i]

    if diferenca_python_10_bilhoes > 0:
        linhas_python_10_bilhoes.append(linhas_python_10_bilhoes[i-1] + diferenca_python_10_bilhoes)
    else:
        linhas_python_10_bilhoes.append(linhas_python_10_bilhoes[i-1])

    if diferenca_c_10_bilhoes > 0:
        linhas_c_10_bilhoes.append(linhas_c_10_bilhoes[i-1] + diferenca_c_10_bilhoes)
    else:
        linhas_c_10_bilhoes.append(linhas_c_10_bilhoes[i-1])

    if diferenca_c_mil > 0:
        linhas_c_mil.append(linhas_c_mil[i-1] + diferenca_c_mil)
    else:
        linhas_c_mil.append(linhas_c_mil[i-1])

    if diferenca_python_mil > 0:
        linhas_python_mil.append(linhas_python_mil[i-1] + diferenca_python_mil)
    else:
        linhas_python_mil.append(linhas_python_mil[i-1])

# Plotando o gráfico em escala logarítmica
plt.figure(figsize=(14, 9))
plt.semilogy(anos, tempo_exec_python_10_bilhoes_segundos, label='Python (velocidade ate contar 10 bilhões)')
plt.semilogy(anos, tempo_exec_c_10_bilhoes_segundos, label='C (velocidade ate contar 10 bilhões)')
plt.semilogy(anos, linhas_python_10_bilhoes, label='Python (Eficiência 10 bilhões)')
plt.semilogy(anos, linhas_c_10_bilhoes, label='C (Eficiência 10 bilhões)')
plt.semilogy(anos, tempo_exec_python_mil_segundos, label='Python (velocidade ate contar mil)')
plt.semilogy(anos, tempo_exec_c_mil_segundos, label='C (velocidade ate contar mil)')
plt.semilogy(anos, linhas_python_mil, label='Python (Eficiência mil)')
plt.semilogy(anos, linhas_c_mil, label='C (Eficiência mil)')
plt.xlabel('Anos')
plt.ylabel('Tempo de Execução (log-scale)')
plt.gca().yaxis.set_major_formatter(FuncFormatter(segundos_formatter))  # Aplicando a formatação dos rótulos

# Adicionando rótulos aos pontos iniciais e finais
for i, ano in enumerate(anos):
    plt.text(ano, tempo_exec_python_10_bilhoes_segundos[i], f'{tempo_exec_python_10_bilhoes_segundos[i]:.3f} s', ha='left', va='bottom')
    plt.text(ano, tempo_exec_c_10_bilhoes_segundos[i], f'{tempo_exec_c_10_bilhoes_segundos[i]:.3f} s', ha='left', va='top')
    plt.text(ano, tempo_exec_python_mil_segundos[i], f'{tempo_exec_python_mil_segundos[i]:.3f} s', ha='left', va='bottom')
    plt.text(ano, tempo_exec_c_mil_segundos[i], f'{tempo_exec_c_mil_segundos[i]:.3f} s', ha='left', va='top')

plt.ylim(1e-9, 1e9) # Valores ajustados para limitar a escala

plt.title('Lei de Moore e Desempenho da linguagem C/Python ao Longo de 10 Anos')
plt.legend()
plt.grid(True)
plt.show()
