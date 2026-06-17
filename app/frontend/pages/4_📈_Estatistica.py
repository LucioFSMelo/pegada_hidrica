"""
ESTAÇÃO: ESTATÍSTICA (FRONTEND)
Esta página lê os dados brutos e monta tabelas de frequência absoluta/relativa
e medidas de tendência central de forma 100% automatizada e independente da turma.
"""

import sys
import os
import streamlit as st
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from app.backend.database import ler_todos_dados

st.set_page_config(page_title="Estação Estatística", page_icon="📈", layout="centered")

st.header("📈 Estação 1: Análise Estatística Geral")
st.markdown("Nesta estação, analisamos a **distribuição estatística dos dados coletados** na escola.")

df_geral = ler_todos_dados()

if df_geral.empty:
    st.warning("📥 Sem dados no banco. Os alunos precisam preencher a calculadora primeiro.")
else:
    # Cálculo dinâmico das medidas centrais pelo Pandas
    st.subheader("📊 Medidas de Tendência Central")
    media_escola = df_geral["gasto_total"].mean()
    mediana_escola = df_geral["gasto_total"].median()
    
    col1, col2 = st.columns(2)
    col1.metric("Média Geral de Consumo", f"{media_escola:.1f} L/dia")
    col2.metric("Mediana de Consumo", f"{mediana_escola:.1f} L/dia")
    
    st.divider()
    
    # --- TABELA DE FREQUÊNCIA DINÂMICA ---
    st.subheader("📊 Tabela de Frequência de Consumo")
    
    # Intervalos de classes fixos pedagógicos para enquadramento dos estudantes
    bins = [0, 50, 100, 150, 200, float('inf')]
    labels = ["Super Econômico (0-50L)", "Consciente (51-100L)", "Moderado (101-150L)", "Alto Gasto (151-200L)", "Desperdício (>200L)"]
    
    df_geral["Faixa de Consumo"] = pd.cut(df_geral["gasto_total"], bins=bins, labels=labels)
    
    # Computa as frequências absoluta e relativa
    freq_absoluta = df_geral["Faixa de Consumo"].value_counts().reindex(labels)
    freq_relativa = (df_geral["Faixa de Consumo"].value_counts(normalize=True) * 100).reindex(labels)
    
    df_frequencia = pd.DataFrame({
        "Frequência Absoluta (Nº de Alunos)": freq_absoluta,
        "Frequência Relativa (%)": freq_relativa.map("{:.1f}%".format)
    })
    
    st.table(df_frequencia)
    
    st.divider()
    
    # --- EXPORTAÇÃO DOS DADOS DA TURMA ---
    st.subheader("📋 Painel de Auditoria de Dados")
    st.markdown("Use a tabela ordenada abaixo para propor exercícios de cálculo manual de média aritmética no caderno:")
    
    # Exibe apenas colunas pertinentes e oculta o ID do banco
    df_filtrado = df_geral[["nome", "turma", "gasto_total"]].sort_values(by="gasto_total").reset_index(drop=True)
    st.dataframe(df_filtrado)
    
    # Exportador nativo para formato CSV (Excel legível)
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Planilha de Dados (.CSV)",
        data=csv,
        file_name="relatorio_detetives_da_agua.csv",
        mime="text/csv"
    )