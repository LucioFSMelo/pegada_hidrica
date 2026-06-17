import sys
import os
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from app.backend.database import login_ou_cadastro_professor, adicionar_turma, buscar_turmas_do_professor, definir_turma_liberada, verificar_turma_liberada, apagar_dados_por_turma

st.set_page_config(page_title="Painel do Professor", page_icon="👨‍🏫")

st.title("👨‍🏫 Central de Comando do Professor")

# Sistema de Login
if "prof_logado" not in st.session_state:
    st.markdown("Faça login para gerenciar suas turmas e liberar o acesso dos alunos.")
    usuario = st.text_input("Usuário (Login):").strip()
    senha = st.text_input("Senha:", type="password").strip()
    
    if st.button("Acessar / Criar Conta"):
        status = login_ou_cadastro_professor(usuario, senha)
        if status == "SENHA_INCORRETA": st.error("❌ Senha incorreta!")
        elif status == "CAMPOS_VAZIOS": st.error("⚠️ Preencha usuário e senha.")
        else:
            st.session_state.prof_logado = usuario
            if status == "NOVO_CADASTRO": st.success("Conta criada! Bem-vindo.")
            st.rerun()
else:
    st.success(f"Logado como: **{st.session_state.prof_logado}**")
    
    # Gerenciamento de Turmas
    st.divider()
    st.subheader("📝 1. Cadastrar Novas Turmas")
    nova_turma = st.text_input("Nome da Turma (Ex: 6º A, 1º Ano EM):").strip()
    if st.button("Cadastrar Turma"):
        if nova_turma:
            if adicionar_turma(st.session_state.prof_logado, nova_turma):
                st.success(f"Turma {nova_turma} cadastrada!")
            else:
                st.error("Turma já existe no sistema.")
        else:
            st.warning("Digite o nome da turma.")
            
    st.divider()
    st.subheader("🔓 2. Liberar Gincana para os Alunos")
    turmas_do_prof = buscar_turmas_do_professor(st.session_state.prof_logado)
    
    status_atual = verificar_turma_liberada()
    st.info(f"**Status atual do aplicativo:** {status_atual}")
    
    if turmas_do_prof:
        turma_selecionada = st.selectbox("Selecione a turma para liberar:", turmas_do_prof)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🟢 ABRIR Acesso", use_container_width=True):
                definir_turma_liberada(turma_selecionada)
                st.success(f"Alunos do {turma_selecionada} agora podem acessar a calculadora!")
                st.rerun()
        with col2:
            if st.button("🔴 FECHAR Acesso", use_container_width=True):
                definir_turma_liberada("FECHADO")
                st.warning("Aplicativo travado para todos os alunos.")
                st.rerun()
        with col3:
            if st.button("🗑️ Zerar Banco desta Turma", use_container_width=True):
                apagar_dados_por_turma(turma_selecionada)
                st.success("Dados apagados.")
    else:
        st.warning("Você ainda não cadastrou nenhuma turma.")
        
    st.divider()
    if st.button("🚪 Sair"):
        del st.session_state.prof_logado
        st.rerun()