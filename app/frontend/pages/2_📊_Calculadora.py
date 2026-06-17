"""
ESTAÇÃO: CALCULADORA (FRONTEND)
Esta página coleta os hábitos de consumo do estudante, aciona o motor de cálculo 
no backend e grava o resultado no banco de dados SQLite associado à turma correta.
"""

import sys
import os
import streamlit as st

# Garante o mapeamento de caminhos para o Python localizar a pasta 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# Importa as funções necessárias do motor e do banco de dados
from app.backend.calculator import calcular_pegada
from app.backend.database import salvar_no_banco, buscar_turmas_ativas

st.set_page_config(page_title="Calculadora de Pegada", page_icon="📊", layout="centered")

# Inicializa o controle de cliques no formulário para evitar envios duplicados
if "dados_enviados" not in st.session_state:
    st.session_state.dados_enviados = False

st.header("📊 Estação de Coleta: Minha Pegada Hídrica")
st.markdown("Preencha seus hábitos diários para calcular o seu consumo estimado de água.")

# Entrada do nome do estudante
nome_aluno = st.text_input("Digite seu primeiro nome:")

# --- BLOCAGEM DE TURMA DINÂMICA ---
# Busca no banco quais turmas os professores já criaram no painel administrativo
turmas_disponiveis = buscar_turmas_ativas()

if turmas_disponiveis:
    # Se existirem turmas cadastradas, exibe um menu de seleção limpo para o aluno
    turma_aluno = st.selectbox("Selecione sua Turma:", turmas_disponiveis)
else:
    # Se o banco estiver zerado (primeiro acesso), permite que o aluno digite livremente
    st.info("💡 Nenhuma turma foi registrada pelos professores ainda. Digite sua turma abaixo:")
    turma_aluno = st.text_input("Digite sua Turma (Ex: 6º Ano A, 3º Ano Médio):").strip()

st.divider()

# Questionário interativo usando Sliders e Radio Buttons
tempo_banho = st.slider("Quanto tempo dura o seu banho diariamente? (minutos)", 1, 30, 10)
chuveiro_fechado = st.radio("Você fecha o chuveiro enquanto se ensaboa?", ("Sim, eu fecho! 🟢", "Não, deixo ligado o tempo todo! 🔴"))

tempo_escovacao = st.slider("Quantos minutos no total você passa escovando os dentes por dia?", 1, 10, 4)
torneira_escovacao = st.radio("Você fecha a torneira enquanto escova os dentes?", ("Sim, sempre fecho! 🟢", "Não, fica aberta! 🔴"))

# Aciona o cálculo vindo do backend
litros_banho, litros_escovacao, litros_total = calcular_pegada(tempo_banho, chuveiro_fechado, tempo_escovacao, torneira_escovacao)

# Exibição dos resultados parciais em formato de cards métricos
st.subheader("🕵️‍♂️ Seu Resultado")
col1, col2 = st.columns(2)
col1.metric("Gasto no Banho", f"{litros_banho:.1f} L")
col2.metric("Gasto na Escovação", f"{litros_escovacao:.1f} L")
st.info(f"**Consumo direto estimado: {litros_total:.1f} litros por dia.**")

# Controle e validação do botão de envio (Trava contra cliques duplos)
if st.session_state.dados_enviados:
    st.success(f"🎉 Seus dados já foram salvos com sucesso! Vá para a página do Ranking para ver a posição da sua turma.")
    if st.button("🔄 Enviar novos dados (Corrigir digitação)"):
        st.session_state.dados_enviados = False
        st.rerun()
else:
    if st.button("💾 Enviar meus dados para o Banco de Dados"):
        if nome_aluno.strip() == "":
            st.error("⚠️ Por favor, digite seu nome antes de enviar!")
        elif str(turma_aluno).strip() == "":
            st.error("⚠️ Por favor, informe ou selecione sua turma antes de enviar!")
        else:
            # Envia para a função de salvamento do database.py
            salvar_no_banco(nome_aluno, turma_aluno, litros_banho, litros_escovacao, litros_total)
            st.session_state.dados_enviados = True
            st.success(f"✅ Sucesso! Dados computados na gincana.")
            st.rerun()