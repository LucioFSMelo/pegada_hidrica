import streamlit as st
import pandas as pd
from app.backend.database import ler_todos_dados

def renderizar_estatistica():
    st.subheader("📈 Análise Estatística Geral")
    df_geral = ler_todos_dados()
    
    if df_geral.empty:
        st.warning("📥 Sem dados no banco para gerar estatísticas.")
    else:
        media_escola = df_geral["gasto_total"].mean()
        mediana_escola = df_geral["gasto_total"].median()
        
        col1, col2 = st.columns(2)
        col1.metric("Média Geral de Consumo", f"{media_escola:.1f} L/dia")
        col2.metric("Mediana de Consumo", f"{mediana_escola:.1f} L/dia")
        
        st.divider()
        st.markdown("#### 📊 Tabela de Frequência de Consumo")
        
        bins = [0, 50, 100, 150, 200, float('inf')]
        labels = ["Super Econômico (0-50L)", "Consciente (51-100L)", "Moderado (101-150L)", "Alto Gasto (151-200L)", "Desperdício (>200L)"]
        
        df_geral["Faixa de Consumo"] = pd.cut(df_geral["gasto_total"], bins=bins, labels=labels)
        freq_absoluta = df_geral["Faixa de Consumo"].value_counts().reindex(labels)
        freq_relativa = (df_geral["Faixa de Consumo"].value_counts(normalize=True) * 100).reindex(labels)
        
        df_frequencia = pd.DataFrame({
            "Frequência Absoluta (Alunos)": freq_absoluta,
            "Frequência Relativa (%)": freq_relativa.map("{:.1f}%".format)
        })
        st.table(df_frequencia)