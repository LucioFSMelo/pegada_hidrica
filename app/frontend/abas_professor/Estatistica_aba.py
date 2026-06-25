import streamlit as st
import pandas as pd
# 🔒 IMPORTAÇÃO COMPATÍVEL: Utilizando a leitura isolada por professor
from app.backend.database import ler_dados_por_professor

def renderizar_estatistica():
    st.subheader("📈 Estação Estatística: Medidas de Tendência Central")
    
    # 🔒 SEGURANÇA: Captura o professor logado para garantir a privacidade dos dados
    prof_atual = st.session_state.get("prof_logado", None)
    
    if not prof_atual:
        st.warning("⚠️ Identificação do professor não localizada. Faça login na Central de Comando.")
        return
    
    # --- BOX PEDAGÓGICO DE CONCEITOS ---
    with st.expander("📚 Ver Definições Matemáticas (Média, Moda e Mediana)"):
        st.markdown("""
        * **Média ($Me$):** É calculada somando todos os valores de um conjunto de dados e dividindo pelo número total de elementos ($n$). É indicada quando os dados são distribuídos uniformemente.
        * **Moda ($Mo$):** Representa o valor mais frequente em um conjunto de dados. Se houver dois valores empatados com maior frequência, o conjunto é chamado de *bimodal*.
        * **Mediana:** É o valor central que divide o conjunto de dados (organizados em ordem crescent ou decrescente) exatamente ao meio (50% dos dados ficam abaixo e 50% ficam acima).
        """)
    
    # 🔒 FILTRO POR PROFESSOR: Busca o consumo das turmas vinculadas ao docente ativo
    df_geral = ler_dados_por_professor(prof_atual)
    
    if df_geral.empty:
        st.warning("📥 Sem dados no banco para gerar as medidas. Peça para os alunos preencherem a calculadora.")
    else:
        # Cálculos Dinâmicos com base EXCLUSIVA na coluna original 'gasto_total'
        media_escola = df_geral["gasto_total"].mean()
        mediana_escola = df_geral["gasto_total"].median()
        
        # Cálculo da Moda tratando casos de distribuição amodal ou multimodal
        moda_serie = df_geral["gasto_total"].mode()
        if moda_serie.empty:
            moda_texto = "Amodal (Nenhum se repete)"
        else:
            moda_texto = ", ".join([f"{val:.1f} L" for val in moda_serie])
            
        # Amplitude Amostral (Valor Máximo - Valor Mínimo)
        amplitude = df_geral["gasto_total"].max() - df_geral["gasto_total"].min()

        # Exibição dos cards estatísticos formatados
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Média Geral ($Me$)", f"{media_escola:.1f} L/dia")
        c2.metric("Mediana", f"{mediana_escola:.1f} L/dia")
        c3.metric("Moda ($Mo$)", moda_texto)
        c4.metric("Amplitude Total", f"{amplitude:.1f} L/dia")
        
        st.divider()
        st.markdown("#### 📊 Tabela de Frequência Combinada (Porcentagem)")
        
        # Distribuição de faixas (Frequência absoluta e relativa) com agrupamento controlado
        bins = [0, 50, 100, 150, 200, float('inf')]
        labels = ["Super Econômico (0-50L)", "Consciente (51-100L)", "Moderado (101-150L)", "Alto Gasto (151-200L)", "Desperdício (>200L)"]
        
        # Gera a categorização das linhas baseadas na coluna real do seu banco
        df_geral["Faixa de Consumo"] = pd.cut(df_geral["gasto_total"], bins=bins, labels=labels)
        freq_absoluta = df_geral["Faixa de Consumo"].value_counts().reindex(labels, fill_value=0)
        freq_relativa = (df_geral["Faixa de Consumo"].value_counts(normalize=True) * 100).reindex(labels, fill_value=0)
        
        # Constrói o DataFrame de exibição para a tabela
        df_frequencia = pd.DataFrame({
            "Frequência Absoluta (Alunos)": freq_absoluta,
            "Frequência Relativa (%)": freq_relativa.map("{:.1f}%".format)
        })
        st.table(df_frequencia)