import sys
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.backend.database import ler_todos_dados, login_ou_cadastro_professor, apagar_dados_por_turma, rotina_autolimpeza_15_dias, buscar_turmas_ativas

st.set_page_config(page_title="Gincana Hídrica", page_icon="🏆", layout="centered")

st.header("🏆 Placar em Tempo Real da Gincana")
df_geral = ler_todos_dados()

if df_geral.empty:
    st.warning("📥 O banco de dados SQLite está vazio. Aguardando o primeiro registro dos estudantes!")
else:
    st.write(f"📊 **Total de participantes registrados:** {len(df_geral)} alunos.")
    
    st.subheader("👑 Os Campeões da Economia (Pódio Dinâmico)")
    
    # Descobre quais turmas possuem dados inseridos no momento
    turmas_com_dados = sorted(df_geral["turma"].unique())
    
    # Monta colunas dinâmicas dependendo de quantas turmas estão ativas na gincana
    if turmas_com_dados:
        cols = st.columns(len(turmas_com_dados))
        for t, col in zip(turmas_com_dados, cols):
            df_turma = df_geral[df_geral["turma"] == t]
            with col:
                st.markdown(f"**📌 {t}**")
                campeao = df_turma.loc[df_turma["gasto_total"].idxmin()]
                st.success(f"🥇 **{campeao['nome']}**\n\n**{campeao['gasto_total']:.1f} L/dia**")

    st.divider()
    st.subheader("📈 Gráfico Comparativo das Médias")
    
    # Calcula as médias dinamicamente agrupando por turma existente
    df_medias = df_geral.groupby("turma")["gasto_total"].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(7, 4))
    # Gera uma paleta de cores azuis dinâmicas para o número de turmas mapeadas
    cores = plt.cm.Blues(pd.np.linspace(0.4, 0.8, len(df_medias))) if hasattr(pd, 'np') else ['#3498db'] * len(df_medias)
    
    barras = ax.bar(df_medias["turma"], df_medias["gasto_total"], color=cores, edgecolor='black', alpha=0.85)
    ax.set_ylabel("Litros Consumidos (Média)", fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.set_ylim(0, max(df_medias["gasto_total"].max() + 30, 150))
    
    for barra in barras:
        altura = barra.get_height()
        ax.annotate(f"{altura:.1f} L", xy=(barra.get_x() + barra.get_width() / 2, altura),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontweight='bold')
        
    st.pyplot(fig)
    plt.close(fig)

# --- PAINEL DO PROFESSOR ATUALIZADO: LOGIN OU CRIAÇÃO DE TURMA ---
st.divider()
with st.expander("🔐 Painel de Gerenciamento do Professor (Acesso / Cadastro)"):
    st.markdown("""
    **Instruções para o Docente:**
    * Caso já possua cadastro, digite seu Usuário e Senha para entrar.
    * Caso seja seu **primeiro acesso**, escolha um nome de Usuário inédito, defina sua Senha e digite a Turma que deseja criar (Ex: *6º ANO C*, *3º ANO SÉRIE B*). O sistema criará sua sala na hora!
    """)
    
    usuario = st.text_input("Usuário do Professor:").strip()
    senha = st.text_input("Senha:", type="password").strip()
    turma_nova = st.text_input("Turma a Criar/Gerenciar (Apenas para novos cadastros):", placeholder="Ex: 6º ANO B").strip()
    
    if st.button("Acessar / Cadastrar Turma"):
        resultado = login_ou_cadastro_professor(usuario, senha, turma_nova)
        
        if resultado == "SENHA_INCORRETA":
            st.error("❌ Usuário existente encontrado, mas a senha digitada está incorreta!")
        elif resultado == "CAMPOS_VAZIOS":
            st.error("⚠️ Para realizar um novo cadastro, preencha Usuário, Senha e o nome da Turma!")
        else:
            st.session_state.logged_prof_turma = resultado
            st.success(f"🔓 Sucesso! Você está gerenciando a turma: **{resultado}**.")
            rotina_autolimpeza_15_dias(resultado)
            st.rerun()

if "logged_prof_turma" in st.session_state:
    st.info(f"Gerenciando atualmente: **{st.session_state.logged_prof_turma}**")
    if st.button(f"🗑️ ZERAR todos os dados do {st.session_state.logged_prof_turma}"):
        apagar_dados_por_turma(st.session_state.logged_prof_turma)
        st.success(f"✅ Dados deletados!")
        st.rerun()
    if st.button("🚪 Sair do Painel"):
        del st.session_state.logged_prof_turma
        st.rerun()