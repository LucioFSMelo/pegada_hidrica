import streamlit as st
import pandas as pd
from app.backend.database import obter_resultados_quiz, zerar_resultados_quiz

def renderizar_aba_resultados_quiz(escola_atual, turma_atual):
    st.markdown(f"## 🏆 Painel de Resultados do Quiz")
    st.caption(f"Exibindo dados em tempo real para: **{escola_atual}** | Turma: **{turma_atual}**")
    
    if not escola_atual or not turma_atual:
        st.warning("⚠️ Por favor, selecione uma Escola e uma Turma nos filtros do painel para carregar os resultados.")
        return

    # 🔄 Carrega os dados do banco
    df_resultados = obter_resultados_quiz(escola_atual, turma_atual)
    
    if df_resultados.empty:
        st.info("ℹ️ Nenhum aluno desta turma realizou o quiz nesta rodada ainda.")
        return

    # Renomeia as colunas para exibição bonita
    df_resultados.columns = ["Nome do Aluno", "Pontuação (Pts)", "Data de Conclusão"]

    # =====================================================================
    # 🥇 SEÇÃO 1: PODIUM / RANKING TOP 3
    # =====================================================================
    st.markdown("### 🥇 Top 3 Melhores Pontuações")
    
    col1, col2, col3 = st.columns(3)
    
    # Tratamento caso a turma tenha menos de 3 alunos que responderam
    qtd_respondidos = len(df_resultados)
    
    with col1:
        if qtd_respondidos >= 1:
            primeiro = df_resultados.iloc[0]
            st.markdown(
                f"""
                <div style="background-color: #f1c40f; padding: 15px; border-radius: 10px; text-align: center; color: black;">
                    <h3>🥇 1º Lugar</h3>
                    <p style="font-size: 18px; font-weight: bold; margin: 5px 0;">{primeiro['Nome do Aluno']}</p>
                    <h2 style="margin: 0;">{primeiro['Pontuação (Pts)']} Pts</h2>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.info("Aguardando líder...")

    with col2:
        if qtd_respondidos >= 2:
            segundo = df_resultados.iloc[1]
            st.markdown(
                f"""
                <div style="background-color: #bdc3c7; padding: 15px; border-radius: 10px; text-align: center; color: black;">
                    <h3>🥈 2º Lugar</h3>
                    <p style="font-size: 16px; font-weight: bold; margin: 5px 0;">{segundo['Nome do Aluno']}</p>
                    <h2 style="margin: 0;">{segundo['Pontuação (Pts)']} Pts</h2>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.text("—")

    with col3:
        if qtd_respondidos >= 3:
            terceiro = df_resultados.iloc[2]
            st.markdown(
                f"""
                <div style="background-color: #e67e22; padding: 15px; border-radius: 10px; text-align: center; color: white;">
                    <h3>🥉 3º Lugar</h3>
                    <p style="font-size: 16px; font-weight: bold; margin: 5px 0;">{terceiro['Nome do Aluno']}</p>
                    <h2 style="margin: 0;">{terceiro['Pontuação (Pts)']} Pts</h2>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.text("—")

    st.divider()

    # =====================================================================
    # 📊 SEÇÃO 2: TABELA COMPLETA DA TURMA
    # =====================================================================
    st.markdown("### 📋 Lista Completa de Classificação")
    st.dataframe(
        df_resultados, 
        use_container_width=True, 
        hide_index=True
    )
    
    st.divider()

    # =====================================================================
    # 🚨 SEÇÃO 3: ZERAR PONTUAÇÕES (ZONA DE PERIGO CONTROLOGADA)
    # =====================================================================
    st.markdown("#### ⚙️ Gerenciamento do Quiz")
    
    # Uso de um st.popover para evitar cliques acidentais que apaguem as notas dos alunos
    with st.popover("🚨 Reiniciar Quiz desta Turma"):
        st.warning(f"Isso apagará permanentemente o histórico de pontos atual da turma '{turma_atual}'. Os alunos poderão refazer o quiz.")
        confirmar_reset = st.checkbox("Estou ciente e quero continuar", key="check_reset_quiz")
        
        if st.button("Sim, Zerar Pontuações!", type="primary", disabled=not confirmar_reset):
            sucesso, msg = zerar_resultados_quiz(escola_atual, turma_atual)
            if sucesso:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)