import streamlit as st
import pandas as pd
import numpy as np

def renderizar_funcoes():
    st.subheader("🧮 Estação Matemática: Modelagem com Funções Afins")
    st.markdown("""
    Nesta estação, os alunos compreendem a equação do consumo de água através de funções matemáticas de 1º Grau:
    $$f(x) = v \cdot x$$
    Onde:
    * $f(x)$ ou $y$: É o consumo final total de água em Litros.
    * $v$: É a vazão constante do equipamento (Chuveiro = 15L/min, Torneira = 6L/min).
    * $x$: É o tempo de uso em minutos (Variável independente).
    """)
    
    equipamento = st.selectbox("Escolha o equipamento para modelar:", ["Chuveiro (Vazão: 15L/min)", "Torneira (Vazão: 6L/min)"])
    vazao = 15.0 if "Chuveiro" in equipamento else 9.0
    
    tempo_limite = st.slider("Projetar gráfico até quantos minutos?", 5, 60, 20)
    
    # Gera dados da função afim para o gráfico
    minutos = np.arange(0, tempo_limite + 1)
    litros = vazao * minutos
    df_funcao = pd.DataFrame({"Tempo (Minutos)": minutos, "Consumo (Litros)": litros})
    
    st.line_chart(df_funcao, x="Tempo (Minutos)", y="Consumo (Litros)")
    st.info(f"Fórmula linear deste gráfico: $$f(x) = {vazao} \cdot x$$")