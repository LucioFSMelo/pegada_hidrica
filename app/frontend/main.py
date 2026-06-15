import sys
import os

# Adiciona a pasta raiz do projeto (pegada_hidrica) ao caminho de busca do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from app.backend.database import inicializar_banco
from app.frontend.view_calc import renderizar_aba_calculadora
from app.frontend.view_ranking import renderizar_aba_ranking
from app.frontend.view_sim import renderizar_aba_simulador

# Configurações globais de página
st.set_page_config(
    page_title="Detetives da Água - Competição Hídrica",
    page_icon="💧",
    layout="centered"
)

# Garante que o banco seja iniciado ao abrir o app
inicializar_banco()

if "dados_enviados" not in st.session_state:
    st.session_state.dados_enviados = False

st.title("💧 Semana do Meio Ambiente: Pegada Hídrica")
st.markdown("""
**8º e 9º anos juntos contra o desperdício!** Calcule sua pegada, envie para o banco de dados e ajude sua turma na gincana!
""")

# Criando as abas de navegação principal
aba1, aba2, aba3 = st.tabs(["📊 Minha Pegada Hídrica", "🏆 Ranking e Pódio", "🚀 Simulador Coletivo"])

with aba1:
    renderizar_aba_calculadora()

with aba2:
    renderizar_aba_ranking()

with aba3:
    renderizar_aba_simulador()