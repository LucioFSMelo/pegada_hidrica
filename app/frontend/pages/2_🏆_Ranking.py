import sys
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.backend.database import ler_todos_dados, verificar_login_professor, apagar_dados_por_turma, rotina_autolimpeza_15_dias
from app.backend.calculator import TURMAS_OFICIAIS

st.set_page_config(page_title="Gincana Hídrica", page_icon="🏆", layout="centered")

st.header("🏆 Placar em Tempo Real da Gincana")
df_geral = ler_todos_dados()

if df_geral.empty:
    st.warning("📥 O banco de dados SQLite está vazio. Aguardando o primeiro registro dos estudantes!")
else:
    st.write(f"📊 **Total de participantes registrados:** {len(df_geral)} alunos.")
    
    st.subheader("👑 Os Campeões da Economia (Pódio por Turma)")
    
    # Renderização do Pódio por Série
    for serie, turmas in zip(["8º Anos", "9º Anos"], [["8º A", "8º B", "8º C"], ["9º A", "9º B", "9º C"]]):
        st.markdown(f"#### **{serie}**")
        cols = st.columns(3)
        for t, col in zip(turmas, cols):
            df_turma = df_geral[df_geral["turma"] == t]
            with col:
                st.markdown(f"**{t}**")
                if df_turma.empty:
                    st.caption("Sem registros")
                else:
                    campeao = df_turma.loc[df_turma["gasto_total"].idxmin()]
                    st.success(f"🥇 **{campeao['nome']}**\n\n**{campeao['gasto_total']:.1f} L/dia**")

    st.divider()
    st.subheader("📈 Gráfico Comparativo das Médias")
    
    df_medias = df_geral.groupby("turma")["gasto_total"].mean().reset_index()
    todas_turmas = pd.DataFrame({"turma": TURMAS_OFICIAIS})
    df_medias = pd.merge(todas_turmas, df_medias, on="turma", how="left").fillna(0)
    
    fig, ax = plt.subplots(figsize=(7, 4))
    barras = ax.bar(df_medias["turma"], df_medias["gasto_total"], color=['#3498db']*3 + ['#2ecc71']*3, edgecolor='black', alpha=0.85)
    ax.set_ylabel("Litros Consumidos (Média)", fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.set_ylim(0, max(df_medias["gasto_total"].max() + 30, 150))
    
    for barra in barras:
        altura = barra.get_height()
        ax.annotate(f"{altura:.1f} L", xy=(barra.get_x() + barra.get_width() / 2, altura),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontweight='bold')
        
    st.pyplot(fig)
    plt.close(fig)

# --- ÁREA DE LOGIN EXCLUSIVA DO PROFESSOR (GERENCIAMENTO DE TURMA) ---
st.divider()
with st.expander("🔐 Painel de Gerenciamento do Professor"):
    st.markdown("Faça login para limpar os dados da sua turma ou verificar a rotina de armazenamento.")
    
    usuario = st.text_input("Usuário do Professor:")
    senha = st.text_input("Senha:", type="password")
    
    if st.button("Acessar Painel"):
        turma_professor = verificar_login_professor(usuario, senha)
        
        if turma_professor:
            st.session_state.logged_prof_turma = turma_professor
            st.success(f"🔓 Bem-vindo! Você tem controle sobre os dados do **{turma_professor}**.")
            
            # Executa a limpeza automática em segundo plano (registros com mais de 15 dias somem)
            rotina_autolimpeza_15_dias(turma_professor)
            st.caption("🔄 A rotina de segurança verificou e removeu dados com mais de 15 dias desta turma.")
        else:
            st.error("❌ Usuário ou senha incorretos!")

# Se o professor estiver logado na sessão, mostra os botões de ação dele
if "logged_prof_turma" in st.session_state:
    st.info(f"Gerenciando atualmente: **{st.session_state.logged_prof_turma}**")
    
    if st.button(f"🗑️ ZERAR todos os dados do {st.session_state.logged_prof_turma}"):
        apagar_dados_por_turma(st.session_state.logged_prof_turma)
        st.success(f"✅ Dados do {st.session_state.logged_prof_turma} apagados com sucesso!")
        st.rerun()
        
    if st.button("🚪 Sair do Painel"):
        del st.session_state.logged_prof_turma
        st.rerun()