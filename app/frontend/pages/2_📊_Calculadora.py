import sys
import os
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from app.backend.calculator import calcular_pegada
from app.backend.database import salvar_no_banco, verificar_turma_liberada

st.set_page_config(page_title="Calculadora", page_icon="📊", layout="centered")

# --- VERIFICAÇÃO DO CADEADO (TRAVA DO PROFESSOR) ---
turma_ativa = verificar_turma_liberada()

if turma_ativa == "FECHADO":
    st.error("⛔ **Acesso Bloqueado!**")
    st.warning("O aplicativo está fechado no momento. Aguarde o seu professor liberar a gincana para a sua turma.")
    st.stop() # Para a execução da página inteira aqui!

# Se chegou aqui, o app está liberado
if "dados_enviados" not in st.session_state:
    st.session_state.dados_enviados = False

st.header("📊 Minha Pegada Hídrica")
st.success(f"🔓 Sala Liberada para: **{turma_ativa}**")

nome_aluno = st.text_input("Digite seu primeiro nome:")

st.divider()
tempo_banho = st.slider("Tempo do banho? (minutos)", 1, 30, 10)
chuveiro_fechado = st.radio("Fecha o chuveiro para ensaboar?", ("Sim, eu fecho! 🟢", "Não, deixo ligado! 🔴"))

tempo_escovacao = st.slider("Tempo escovando dentes? (minutos)", 1, 10, 4)
torneira_escovacao = st.radio("Fecha a torneira ao escovar?", ("Sim, sempre fecho! 🟢", "Não, fica aberta! 🔴"))

litros_banho, litros_escovacao, litros_total = calcular_pegada(tempo_banho, chuveiro_fechado, tempo_escovacao, torneira_escovacao)

st.subheader("🕵️‍♂️ Seu Resultado")
col1, col2 = st.columns(2)
col1.metric("Gasto Banho", f"{litros_banho:.1f} L")
col2.metric("Gasto Escovação", f"{litros_escovacao:.1f} L")
st.info(f"**Total Diário Estimado: {litros_total:.1f} litros.**")

if st.session_state.dados_enviados:
    st.success("🎉 Seus dados foram salvos! Confira o Ranking.")
else:
    if st.button("💾 Enviar meus dados"):
        if nome_aluno.strip() == "":
            st.error("Digite seu nome!")
        else:
            # Salva automaticamente na turma que o professor liberou!
            salvar_no_banco(nome_aluno, turma_ativa, litros_banho, litros_escovacao, litros_total)
            st.session_state.dados_enviados = True
            st.rerun()