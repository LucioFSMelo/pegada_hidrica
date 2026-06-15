VAZAO_CHUVEIRO = 15
VAZAO_TORNEIRA_PIA = 9
TURMAS_OFICIAIS = ["8º A", "8º B", "8º C", "9º A", "9º B", "9º C"]

def calcular_pegada(tempo_banho, chuveiro_fechado, tempo_escovacao, torneira_escovacao):
    """Calcula os litros gastos baseados nos hábitos informados."""
    if "Sim" in chuveiro_fechado:
        tempo_chuveiro_ligado = tempo_banho / 2
    else:
        tempo_chuveiro_ligado = tempo_banho
    litros_banho = tempo_chuveiro_ligado * VAZAO_CHUVEIRO

    if "Sim" in torneira_escovacao:
        litros_escovacao = 0.5 * VAZAO_TORNEIRA_PIA
    else:
        litros_escovacao = tempo_escovacao * VAZAO_TORNEIRA_PIA

    litros_total = litros_banho + litros_escovacao
    return litros_banho, litros_escovacao, litros_total

def calcular_economia_coletiva(tamanho_turma):
    """Calcula a simulação de economia mensal de uma turma."""
    gasto_antigo = 12 * VAZAO_CHUVEIRO 
    gasto_novo = 6 * VAZAO_CHUVEIRO 
    economia_mes = (gasto_antigo - gasto_novo) * tamanho_turma * 30
    return economia_mes