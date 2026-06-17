import streamlit as st
import pandas as pd
from app.backend.database import ler_todos_dados

def renderizar_ranking():
    st.subheader("🏆 Placar da Gincana Hídrica")
    df_geral = ler_todos_dados()
    
    if df_geral.empty:
        st.warning("📥 O banco de dados está vazio. Os alunos precisam preencher a calculadora primeiro.")
    else:
        # Agrupa o consumo total por turma e calcula a média
        ranking_turmas = df_geral.groupby("turma")["gasto_total"].mean().reset_index()
        ranking_turmas = ranking_turmas.sort_values(by="gasto_total", ascending=True).reset_index(drop=True)
        
        st.markdown("### 🥇 Ranking das Turmas Mais Econômicas (Menor Média vence!)")
        
        for i, linha in ranking_turmas.iterrows():
            medalha = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else " Bustos "
            st.info(f"**{i+1}º Lugar {medalha}**: {linha['turma']} — Média de **{linha['gasto_total']:.1f} Litros** por aluno.")
            
        st.divider()
        st.markdown("#### 📊 Gráfico Comparativo das Turmas")
        st.bar_chart(data=ranking_turmas, x="turma", y="gasto_total")