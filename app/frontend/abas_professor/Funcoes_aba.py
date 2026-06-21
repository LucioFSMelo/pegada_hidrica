import streamlit as st
import pandas as pd
import numpy as np
from app.backend.database import ler_todos_dados

def renderizar_funcoes():
    st.subheader("🎲 Estação Probabilidade e Simulação de Eventos")
    
    # --- BOX PEDAGÓGICO DE CONCEITOS ---
    with st.expander("📚 Ver Fundamentos de Probabilidade (BNCC)"):
        st.markdown("""
        * **Espaço Amostral ($\Omega$):** Conjunto formado por todos os resultados possíveis de um experimento aleatório.
        * **Evento ($A$):** É um subconjunto do espaço amostral.
        * **Cálculo da Probabilidade:** A probabilidade de um evento $A$ ocorrer em um espaço equiprovável é dada pela razão:
        $$P(A) = \\frac{n(A)}{n(\\Omega)} = \\frac{\\text{Casos Favoráveis}}{\\text{Casos Possíveis}}$$
        * A probabilidade é sempre um valor de $0$ (evento impossível) a $1$ (evento certo), expressa frequentemente em formato percentual (%).
        """)

    df_geral = ler_todos_dados()
    
    if df_geral.empty:
        st.warning("📥 É necessário ter dados cadastrados na gincana para rodar as simulações probabilísticas reais.")
    else:
        st.markdown("### 🔮 Simulador: O Sorteio Aleatório de Alunos")
        st.markdown("""
        Imagine a situação: se o professor sortear **um aluno ao acaso** dentro desta gincana para ser o líder ecológico, 
        quais são as chances probabilísticas baseadas nos comportamentos atuais da turma?
        """)
        
        # Espaço amostral n(Omega)
        total_alunos = len(df_geral)
        
        # Eventos categorizados
        alunos_economicos = len(df_geral[df_geral["gasto_total"] <= 110])
        alunos_desperdicio = len(df_geral[df_geral["gasto_total"] > 110])
        
        prob_eco = (alunos_economicos / total_alunos) * 100
        prob_desp = (alunos_desperdicio / total_alunos) * 100
        
        st.info(f"**Tamanho do Espaço Amostral ($n(\\Omega)$):** {total_alunos} alunos participando.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Probabilidade de Sortear Aluno Econômico (≤ 110L)", f"{prob_eco:.1f}%")
            st.caption(f"Casos favoráveis $n(A)$: {alunos_economicos} alunos")
        with c2:
            st.metric("Probabilidade de Sortear Aluno Alto Gasto (> 110L)", f"{prob_desp:.1f}%")
            st.caption(f"Casos favoráveis $n(B)$: {alunos_desperdicio} alunos")
            
        st.divider()
        st.markdown("### 📉 Simulação de Cenários de Economia (Porcentagem Aplicada)")
        st.markdown("Se aplicarmos uma intervenção educativa e **toda a turma** reduzir seu tempo de consumo diário, o que acontece?")
        
        meta_reducao = st.slider("Escolha uma meta de redução percentual (%) para simulação:", 5, 50, 20)
        
        consumo_atual_total = df_geral["gasto_total"].sum()
        consumo_projetado_total = consumo_atual_total * (1 - (meta_reducao / 100))
        economia_litros = consumo_atual_total - consumo_projetado_total
        
        col_at, col_pr, col_ec = st.columns(3)
        col_at.metric("Consumo Atual Total", f"{consumo_atual_total:.1f} L")
        col_pr.metric(f"Projeção (-{meta_reducao}%)", f"{consumo_projetado_total:.1f} L")
        col_ec.metric("Água Salva na Simulação", f"{economia_litros:.1f} L", delta="Econômico", delta_color="inverse")