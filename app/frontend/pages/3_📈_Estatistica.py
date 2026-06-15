import sys
import os
import streamlit as st
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from app.backend.database import ler_todos_dados

st.set_page_config(page_title="Estação Estatística", page_icon="📈", layout="centered")

st.header("📈 Estação 1: Análise Estatística e Auditoria")
st.markdown("""
Nesta estação, vamos analisar a **distribuição dos dados coletados** e gerar tabelas de frequência.
Professores podem usar esses dados reais para ensinar Média, Mediana e Moda em sala!
""")

df_geral = ler_todos_dados()

if df_geral.empty:
    st.warning("📥 Sem dados no banco. Os alunos precisam preencher a calculadora primeiro.")
else:
    # --- MÉTRICAS GERAIS DA ESCOLA ---
    st.subheader("📊 Medidas de Tendência Central (Escola)")
    media_escola = df_geral["gasto_total"].mean()
    mediana_escola = df_geral["gasto_total"].median()
    
    col1, col2 = st.columns(2)
    col1.metric("Média Geral de Consumo", f"{media_escola:.1f} L/dia")
    col2.metric("Mediana de Consumo", f"{mediana_escola:.1f} L/dia")
    
    st.divider()
    
    # --- TABELA DE FREQUÊNCIA POR INTERVALO DE CLASSE ---
    st.subheader("📊 Tabela de Frequência de Consumo")
    st.markdown("Quantos alunos se enquadram em cada faixa de gasto diário?")
    
    # Define os limites das faixas de consumo (Intervalos de classe)
    bins = [0, 50, 100, 150, 200, float('inf')]
    labels = ["Super Econômico (0-50L)", "Consciente (51-100L)", "Moderado (101-150L)", "Alto Gasto (151-200L)", "Desperdício (>200L)"]
    
    # Corta e categoriza os dados brutos usando o Pandas
    df_geral["Faixa de Consumo"] = pd.cut(df_geral["gasto_total"], bins=bins, labels=labels)
    
    # Cria a tabela de frequência absoluta e relativa (porcentagem)
    freq_absoluta = df_geral["Faixa de Consumo"].value_counts().reindex(labels)
    freq_relativa = (df_geral["Faixa de Consumo"].value_counts(normalize=True) * 100).reindex(labels)
    
    df_frequencia = pd.DataFrame({
        "Frequência Absoluta (Nº de Alunos)": freq_absoluta,
        "Frequência Relativa (%)": freq_relativa.map("{:.1f}%".format)
    })
    
    st.table(df_frequencia)
    
    st.divider()
    
    # --- EXPORTAÇÃO DE DADOS ---
    st.subheader("📋 Dados Brutos Ordenados (Auditoria)")
    st.markdown("Use o botão abaixo para baixar a tabela em formato Excel/CSV para fazer cálculos no caderno.")
    
    df_filtrado = df_geral[["nome", "turma", "gasto_total"]].sort_values(by="gasto_total").reset_index(drop=True)
    st.dataframe(df_filtrado)
    
    # Converte o dataframe para CSV para download nativo do Streamlit
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Dados das Turmas (Arquivo .CSV)",
        data=csv,
        file_name="dados_pegada_hidrica_escola.csv",
        mime="text/csv"
    )