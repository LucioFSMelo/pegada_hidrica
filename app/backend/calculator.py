"""
MÓDULO BACKEND: CALCULATOR
Este arquivo é o motor de cálculo do sistema. Ele não armazena dados, 
apenas processa as fórmulas matemáticas de consumo hídrico com base 
nos coeficientes de vazão padrão recomendados por órgãos de saneamento.
"""

# Constantes de vazão (Litros por minuto)
VAZAO_CHUVEIRO = 15.0       
VAZAO_TORNEIRA_PIA = 6.0    

def calcular_pegada(tempo_banho, chuveiro_fechado, tempo_escovacao, torneira_escovacao):
    # Banho
    if "Sim" in chuveiro_fechado:
        litros_banho = tempo_banho * VAZAO_CHUVEIRO * 0.5
    else:
        litros_banho = tempo_banho * VAZAO_CHUVEIRO

    # Escovação (10% do gasto se fechar a torneira)
    if "Sim" in torneira_escovacao:
        litros_escovacao = tempo_escovacao * VAZAO_TORNEIRA_PIA * 0.10
    else:
        litros_escovacao = tempo_escovacao * VAZAO_TORNEIRA_PIA

    litros_total = litros_banho + litros_escovacao
    return litros_banho, litros_escovacao, litros_total