import streamlit as st
import pandas as pd
# Importamos as funções originais do seu banco de dados
from app.backend.database import (
    ler_dados_por_professor, 
    buscar_turmas_do_professor, 
    obter_ranking_melhores_turmas
)

def renderizar_ranking():
    st.subheader("🏆 Placar da Gincana Hídrica")
    
    # 🔒 Recupera o professor logado na sessão para isolar os dados
    prof_atual = st.session_state.get("prof_logado", None)
    
    if not prof_atual:
        st.warning("⚠️ Identificação do professor não localizada. Faça login na Central de Comando.")
        return

    # 1. CARREGA O RANKING DAS TURMAS
    ranking_turmas = obter_ranking_melhores_turmas(prof_atual)
    
    if ranking_turmas.empty:
        st.warning("📥 O banco de dados está vazio para as suas turmas. Os alunos precisam preencher a calculadora primeiro.")
    else:
        st.markdown("### 🥇 Ranking das Turmas Mais Econômicas (Menor Média vence!)")
        
        # Renderização das medalhas por média de consumo
        for i, linha in ranking_turmas.reset_index(drop=True).iterrows():
            medalha = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🏅"
            st.info(
                f"**{i+1}º Lugar {medalha}**: {linha['turma']} — "
                f"Média de **{linha['media_consumo']:.1f} Litros** por aluno "
                f"({int(linha['total_alunos'])} investigadores)."
            )
            
        # Exibe o gráfico de barras comparativo entre as turmas do professor
        st.divider()
        st.markdown("#### 📊 Gráfico Comparativo das Turmas")
        st.bar_chart(data=ranking_turmas, x="turma", y="media_consumo")
        
        # =====================================================================
        # 🕵️‍♂️ RANKING DOS ALUNOS MAIS ECONÔMICOS
        # =====================================================================
        st.divider()
        st.markdown("### 🏆 Ranking dos Alunos Mais Econômicos")
        st.markdown("Descubra quais detetives estão liderando a pontuação de economia hídrica individual:")
        
        # Busca apenas as turmas deste professor para preencher o filtro
        turmas_do_prof = buscar_turmas_do_professor(prof_atual)
        opcoes_filtro = ["Geral (Todas as minhas turmas)"] + turmas_do_prof
        
        filtro_aluno = st.selectbox(
            "Filtrar ranking de alunos por:", 
            opcoes_filtro, 
            key="filtro_ranking_alunos_aba"
        )
        
        # Carrega o DataFrame bruto de consumo dos alunos (apenas deste professor)
        df_alunos = ler_dados_por_professor(prof_atual)
        
        if not df_alunos.empty:
            # Aplica o filtro caso o usuário escolha uma turma específica
            if filtro_aluno != "Geral (Todas as minhas turmas)":
                df_filtrado = df_alunos[df_alunos["turma"] == filtro_aluno]
            else:
                df_filtrado = df_alunos
                
            if not df_filtrado.empty:
                # Ordena os alunos do menor gasto para o maior usando a coluna 'gasto_total'
                df_ranking_alunos = df_filtrado.sort_values(by="gasto_total", ascending=True).reset_index(drop=True)
                df_ranking_alunos.index += 1 # Ajusta o índice para exibir 1º, 2º...
                
                # Mapeia os nomes das colunas originais do seu banco para exibição na tabela
                df_exibicao = df_ranking_alunos[["nome", "turma", "gasto_total"]].copy()
                df_exibicao.columns = ["Detetive 🕵️‍♂️", "Turma 🏫", "Consumo Total (Litros) 💧"]
                
                # Desenha a tabela estilizada
                st.dataframe(df_exibicao, use_container_width=True)
                
                # Mensagem honorária para o líder do ranking selecionado
                lider_atual = df_ranking_alunos.iloc[0]
                st.success(
                    f"🌟 **Destaque:** O detetive **{lider_atual['nome']}** da turma **{lider_atual['turma']}** "
                    f"está liderando com um consumo exemplar de apenas **{lider_atual['gasto_total']:.1f} Litros**!"
                )
            else:
                st.info(f"Nenhum aluno da turma '{filtro_aluno}' realizou o envio de dados até o momento.")
        else:
            st.info("Nenhum dado de consumo individual localizado.")