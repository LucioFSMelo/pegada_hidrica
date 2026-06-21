import streamlit as st
from app.backend.database import ler_todos_dados

def renderizar_dicas():
    st.subheader("💡 Estação de Missões Econômicas: Evitando o Desperdício")
    st.markdown("""
    Com base no nosso manual tático **Missão: Detetives da Água**, o consumo direto vem de ações cotidianas. 
    Abaixo, escolha quais missões de economia você quer propor para simular o impacto coletivo na escola!
    """)
    
    df_geral = ler_todos_dados()
    total_alunos = len(df_geral) if not df_geral.empty else 30 # Caso esteja vazio, assume uma turma padrão de 30 para visualização
    
    st.markdown(f"### 📋 Simulação com base em **{total_alunos} alunos**")
    
    # --- MISSÃO 1: REDUÇÃO NO BANHO (Baseado no cenário do PDF) ---
    st.markdown("#### 🧼 Missão 1: Operação Banho Cronometrado")
    st.caption("No manual, vimos que diminuir o tempo de banho ou fechar o chuveiro ao se ensaboar reduz drasticamente o desperdício (vazão de 15 L/min).")
    minutos_economizados = st.slider("Quantos minutos de banho cada aluno vai reduzir por dia?", 0, 15, 5, key="dica_banho")
    
    # Cálculo: minutos * vazão (15L/min) * total de alunos
    economia_banho_aluno = minutos_economizados * 15
    economia_banho_turma = economia_banho_aluno * total_alunos
    
    # --- MISSÃO 2: TORNEIRA FECHADA (Baseado na página 8 do PDF) ---
    st.markdown("#### 🪥 Missão 2: Torneira Blindada na Escovação")
    st.caption("Uma torneira aberta gasta cerca de 6 litros por minuto. Escovar os dentes com a torneira fechada salva muita água.")
    fechar_torneira = st.checkbox("Engajar a turma para fechar 100% a torneira ao escovar os dentes? (Economiza ~4 minutos ou 24L por dia por aluno)", value=True)
    
    economia_torneira_aluno = 24 if fechar_torneira else 0
    economia_torneira_turma = economia_torneira_aluno * total_alunos
    
    # --- RESULTADOS CONSOLIDADOS ---
    st.divider()
    st.markdown("### 🏆 Resultado Projetado da Mobilização Coletiva")
    
    total_economizado_dia = economia_banho_turma + list([economia_torneira_turma])[0]
    total_economizado_mes = total_economizado_dia * 30
    
    # Metáfora visual pedagógica: Caixas d'água de 1000 Litros
    caixas_salvas = total_economizado_mes / 1000
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Economia Diária da Turma", f"{total_economizado_dia:.0f} Litros")
    c2.metric("Economia Mensal da Turma", f"{total_economizado_mes:.0f} Litros")
    c3.metric("Caixas d'Água Salvas (1000L)", f"{caixas_salvas:.1f} unidades", delta="Meta Ecológica")
    
    # Card de dicas textuais diretas do PDF para fixação
    st.success("""
    **💡 Dicas de Ouro dos Detetives da Água para levar para casa:**
    1. **Chuveiro:** Não use o banho como momento de reflexão. 5 a 10 minutos são suficientes.
    2. **Torneira:** Abra apenas para molhar e enxaguar a boca/mãos. Mantenha fechada enquanto ensaboa ou escova.
    3. **Vazamentos:** Uma torneira pingando pode desperdiçar mais de 40 litros por dia. Avise imediatamente um adulto!
    """)