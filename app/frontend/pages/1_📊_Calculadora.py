import sys
import os
import streamlit as st

# Garante que o Python encontre a pasta raiz 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.backend.calculator import calcular_pegada, TURMAS_OFICIAIS
from app.backend.database import salvar_no_banco

st.set_page_config(page_title="Calculadora de Pegada", page_icon="📊", layout="centered")

# Inicializa o controle de clique único para esta página/aba do navegador
if "dados_enviados" not in st.session_state:
    st.session_state.dados_enviados = False

st.header("📊 Estação de Coleta: Minha Pegada Hídrica")
st.markdown("Preencha o formulário abaixo com seus hábitos diários para calcular o seu consumo estimado.")

nome_aluno = st.text_input("Digite seu primeiro nome:")
turma_aluno = st.selectbox("Selecione sua turma:", TURMAS_OFICIAIS)

st.divider()

tempo_banho = st.slider("Quanto tempo dura o seu banho diariamente? (minutos)", 1, 30, 10)
chuveiro_fechado = st.radio("Você fecha o chuveiro enquanto se ensaboa?", ("Sim, eu fecho! 🟢", "Não, deixo ligado o tempo todo! 🔴"))

tempo_escovacao = st.slider("Quantos minutos no total você passa escovando os dentes por dia?", 1, 10, 4)
torneira_escovacao = st.radio("Você fecha a torneira enquanto escova os dentes?", ("Sim, sempre fecho! 🟢", "Não, fica aberta! 🔴"))

# Executa o cálculo vindo do backend
litros_banho, litros_escovacao, litros_total = calcular_pegada(tempo_banho, chuveiro_fechado, tempo_escovacao, torneira_escovacao)

st.subheader("🕵️‍♂️ Seu Resultado")
col1, col2 = st.columns(2)
col1.metric("Gasto no Banho", f"{litros_banho:.1f} L")
col2.metric("Gasto na Escovação", f"{litros_escovacao:.1f} L")
st.info(f"**Consumo direto estimado: {litros_total:.1f} litros por dia.**")

# Trava contra cliques duplos
if st.session_state.dados_enviados:
    st.success(f"🎉 Seus dados já foram salvos, {nome_aluno}! Vá para a página do Ranking para ver a posição da sua turma.")
    if st.button("🔄 Enviar novos dados (Corrigir digitação)"):
        st.session_state.dados_enviados = False
        st.rerun()
else:
    if st.button("💾 Enviar meus dados para o Banco de Dados"):
        if nome_aluno.strip() == "":
            st.error("⚠️ Por favor, digite seu nome antes de enviar!")
        else:
            salvar_no_banco(nome_aluno.strip(), turma_aluno, litros_banho, litros_escovacao, litros_total)
            st.session_state.dados_enviados = True
            st.success(f"✅ Sucesso! Dados salvos no banco SQLite.")
            st.rerun()