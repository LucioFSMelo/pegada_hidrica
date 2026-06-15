import streamlit as st
from app.backend.calculator import calcular_economia_coletiva

def renderizar_aba_simulador():
    st.header("🌍 O Poder do Coletivo")
    tamanho_turma = st.slider("Tamanho da turma para simulação:", 10, 45, 30)
    
    # Puxa a regra matemática do backend
    economia_mes = calcular_economia_coletiva(tamanho_turma)

    st.metric("Economia Estimada por MÊS", f"{int(economia_mes):,} Litros")
    st.write(f"Isso equivale a **{int(economia_mes / 1000)} caixas d'água** de 1.000 litros cheias na Mirueira!")