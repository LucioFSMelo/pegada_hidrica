"""
MÓDULO BACKEND: CALCULATOR
Este arquivo é o motor de cálculo do sistema. Ele não armazena dados, 
apenas processa as fórmulas matemáticas de consumo hídrico com base 
nos coeficientes de vazão padrão recomendados por órgãos de saneamento.
"""

# Constantes de vazão (Litros por minuto)
VAZAO_CHUVEIRO = 15.0       # Média de consumo de um chuveiro comum por minuto
VAZAO_TORNEIRA_PIA = 9.0    # Média de consumo de uma torneira de pia por minuto

def calcular_pegada(tempo_banho, chuveiro_fechado, tempo_escovacao, torneira_escovacao):
    """
    Realiza o cálculo da pegada hídrica diária direta do estudante.
    
    Parâmetros:
    - tempo_banho (int): Tempo em minutos gasto no banho.
    - chuveiro_fechado (str): Resposta se fecha o chuveiro ao se ensaboar.
    - tempo_escovacao (int): Tempo em minutos escovando os dentes.
    - torneira_escovacao (str): Resposta se fecha a torneira ao escovar.
    
    Retorna:
    - litros_banho (float): Total gasto no banho.
    - litros_escovacao (float): Total gasto na escovação.
    - litros_total (float): Soma total do consumo diário do aluno.
    """
    
    # 1. Cálculo do Banho
    # Se o aluno fecha o chuveiro enquanto se ensaboa, estimamos pedagogicamente 
    # que ele reduz o tempo de fluxo de água pela metade (0.5)
    if "Sim" in chuveiro_fechado:
        litros_banho = tempo_banho * VAZAO_CHUVEIRO * 0.5
    else:
        litros_banho = tempo_banho * VAZAO_CHUVEIRO

    # 2. Cálculo da Escovação de Dentes
    # Se o aluno fecha a torneira enquanto escova, o gasto é mínimo (apenas 1 litro para enxágue)
    if "Sim" in torneira_escovacao:
        litros_escovacao = 1.0
    else:
        litros_escovacao = tempo_escovacao * VAZAO_TORNEIRA_PIA

    # 3. Cálculo Total
    litros_total = litros_banho + litros_escovacao

    return litros_banho, litros_escovacao, litros_total