import sys
import os
import streamlit as st

# --- GARANTIA DE CAMINHOS ABSOLUTOS ---
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__)) 
PASTA_FRONTEND = os.path.dirname(DIRETORIO_ATUAL)            
PASTA_APP = os.path.dirname(PASTA_FRONTEND)                 
RAIZ_PROJETO = os.path.dirname(PASTA_APP)                   

if RAIZ_PROJETO not in sys.path:
    sys.path.insert(0, RAIZ_PROJETO)

# --- IMPORTS DO BACKEND ---
from app.backend.database import (
    login_ou_cadastro_professor, 
    adicionar_turma, 
    buscar_turmas_do_professor, 
    definir_turma_liberada, 
    verificar_turma_liberada, 
    apagar_dados_por_turma
)

# --- IMPORTS EXCLUSIVOS DAS ABAS DO PROFESSOR (MODULARIZADOS) ---
from app.frontend.abas_professor.Calculadora_aba import renderizar_calculadora
from app.frontend.abas_professor.Ranking_aba import renderizar_ranking
from app.frontend.abas_professor.Estatistica_aba import renderizar_estatistica
from app.frontend.abas_professor.Funcoes_aba import renderizar_funcoes
from app.frontend.abas_professor.Financeiro_aba import renderizar_financeiro
from app.frontend.abas_professor.Dicas_aba import renderizar_dicas

st.set_page_config(page_title="Painel do Professor", page_icon="👨‍🏫", layout="wide")

st.title("👨‍🏫 Central de Comando do Professor")

# --- CONTROLE DE ACESSO ---
if "prof_logado" not in st.session_state:
    st.markdown("### 🔐 Área Restrita do Orientador")
    usuario = st.text_input("Usuário (Login):").strip()
    senha = st.text_input("Senha:", type="password").strip()
    
    if st.button("Acessar / Criar Conta", use_container_width=True):
        status = login_ou_cadastro_professor(usuario, senha)
        if status == "SENHA_INCORRETA": st.error("❌ Senha incorreta!")
        elif status == "CAMPOS_VAZIOS": st.error("⚠️ Preencha usuário e senha.")
        else:
            st.session_state.prof_logado = usuario
            st.rerun()
else:
    # --- INTERFACE PRINCIPAL DO PAINEL DO PROFESSOR ---
    st.sidebar.success(f"Sessão Ativa: {st.session_state.prof_logado}")
    if st.sidebar.button("🚪 Sair do Painel"):
        del st.session_state.prof_logado
        st.rerun()

    # Criação das abas visuais estilo Bootstrap/Dashboard
    aba_gerenciar, aba_calc, aba_rank, aba_estat, aba_func, aba_finan, aba_dicas = st.tabs([
        "⚙️ Gerenciar Gincana", 
        "📊 Calculadora", 
        "🏆 Ranking", 
        "📈 Estatística", 
        "🧮 Funções", 
        "💰 Financeiro",
        "💡 Dicas e Missões"
    ])

    # Injeção de cada módulo dentro de sua respectiva Aba
    with aba_gerenciar:
        st.subheader("⚙️ Configurações Gerais")
        col_c, col_l = st.columns(2)
        with col_c:
            st.markdown("#### 📝 Cadastrar Turma")
            nova_turma = st.text_input("Nome (Ex: 6º ANO B):").strip()
            if st.button("Cadastrar", use_container_width=True):
                if nova_turma and adicionar_turma(st.session_state.prof_logado, nova_turma):
                    st.success("Cadastrada!")
                    st.rerun()
                else: st.error("Turma já existente ou campo vazio.")
        with col_l:
            st.markdown("#### 🔓 Liberar para os Alunos")
            turmas_do_prof = buscar_turmas_do_professor(st.session_state.prof_logado)
            st.metric("Status Atual:", verificar_turma_liberada())
            if turmas_do_prof:
                t_sel = st.selectbox("Selecione a turma:", turmas_do_prof)
                if st.button("🟢 ABRIR Acesso", use_container_width=True):
                    definir_turma_liberada(t_sel)
                    st.rerun()
                if st.button("🔴 FECHAR Acesso", use_container_width=True):
                    definir_turma_liberada("FECHADO")
                    st.rerun()
                if st.button(f"🗑️ Zerar Banco do {t_sel}", use_container_width=True):
                    apagar_dados_por_turma(t_sel)
                    st.success("Zerado!")

    with aba_calc:
        renderizar_calculadora()

    with aba_rank:
        renderizar_ranking()

    with aba_estat:
        renderizar_estatistica()

    with aba_func:
        renderizar_funcoes()

    with aba_finan:
        renderizar_financeiro()

    with aba_dicas:
        renderizar_dicas()