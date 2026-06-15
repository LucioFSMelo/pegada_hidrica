import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from app.backend.database import ler_todos_dados, apagar_banco
from app.backend.calculator import TURMAS_OFICIAIS

def renderizar_aba_ranking():
    df_geral = ler_todos_dados()
    
    if df_geral.empty:
        st.warning("📥 O banco de dados SQLite está vazio. Aguardando registros!")
        return

    st.write(f"📊 **Total de participantes registrados no banco:** {len(df_geral)} alunos.")
    st.subheader("👑 Os Campeões da Economia (Pódio por Turma)")
    
    # Renderização dos pódios por série
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
    st.subheader("📈 Placar Geral das Turmas")
    
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
    
    st.subheader("📋 Tabela Geral de Auditoria")
    st.dataframe(df_geral[["nome", "turma", "gasto_total"]].sort_values(by="gasto_total"))

    # Painel do Professor protegido
    st.divider()
    with st.expander("⚙️ Painel de Controle do Professor"):
        senha_professor = st.text_input("Digite a senha de administrador:", type="password", key="senha_prof")
        if senha_professor == "admin123":
            st.success("🔓 Acesso liberado, Professor!")
            if st.button("🗑️ Resetar Gincana (Apagar Banco SQLite)"):
                apagar_banco()
                st.rerun()
        elif senha_professor:
            st.error("❌ Senha incorreta!")