import streamlit as st
from app.backend.calculator import calcular_pegada
from app.backend.database import salvar_no_banco, verificar_turma_liberada

def renderizar_calculadora():
    st.subheader("📊 Estação de Coleta: Pegada Hídrica")
    
    # Verifica qual turma está destrancada no sistema
    turma_ativa = verificar_turma_liberada()
    
    if turma_ativa == "FECHADO":
        st.error("⛔ A calculadora está travada. Ative ou libere uma turma na aba 'Gerenciar Gincana' primeiro!")
    else:
        st.success(f"🔓 Pronto para coletar dados da turma: **{turma_ativa}**")
        
        # Controle de estado para saber se o aluno já enviou os dados
        if "dados_enviados" not in st.session_state:
            st.session_state.dados_enviados = False
            
        nome_aluno = st.text_input("Digite o primeiro nome do aluno (Detetive):")
        
        st.divider()
        
        # Substituímos o slider pelo number_input para permitir digitação livre
        t_banho = st.number_input("Tempo de banho diário (minutos):", min_value=0, value=10, step=1, key="calc_banho")
        c_fechado = st.radio("Fecha o chuveiro ao se ensaboar?", ("Sim, eu fecho! 🟢", "Não, deixo ligado! 🔴"), key="calc_chuveiro")
        
        t_escova = st.number_input("Minutos gastos escovando os dentes por dia:", min_value=0, value=4, step=1, key="calc_escova")
        t_fechada = st.radio("Fecha a torneira ao escovar os dentes?", ("Sim, sempre fecho! 🟢", "Não, fica aberta! 🔴"), key="calc_torneira")
        
        # O backend faz o cálculo matemático
        l_banho, l_escova, l_total = calcular_pegada(t_banho, c_fechado, t_escova, t_fechada)
        
        st.markdown("##### Resultado do Aluno:")
        col_b, col_e, col_t = st.columns(3)
        col_b.metric("Banho", f"{l_banho:.1f} L")
        col_e.metric("Escovação", f"{l_escova:.1f} L")
        col_t.metric("Total Diário", f"{l_total:.1f} L")
        
        # Controle de tela pós-envio
        if st.session_state.dados_enviados:
            st.success("✅ Dados gravados com sucesso no Placar da Gincana!")
            if st.button("🔄 Coletar dados do próximo aluno"):
                st.session_state.dados_enviados = False
                st.rerun()
        else:
            if st.button("💾 Salvar Registro no Banco de Dados", use_container_width=True):
                
                # ==========================================================
                # 🚨 BARREIRA DE VALIDAÇÃO PEDAGÓGICA (PROPOSTA 2)
                # ==========================================================
                if nome_aluno.strip() == "":
                    st.error("⚠️ Identificação necessária! Por favor, digite o nome do aluno.")
                    
                elif t_banho > 60:
                    st.warning(
                        f"🕵️‍♂️ **Alerta do Esquadrão:** Um banho de **{t_banho} minutos** indica um grande desperdício "
                        "ou um erro de digitação! Verifique se você mediu corretamente o seu tempo."
                    )
                    
                elif t_escova > 15:
                    st.warning(
                        f"🕵️‍♂️ **Alerta do Esquadrão:** **{t_escova} minutos** escovando os dentes? Isso gastaria "
                        "muita água! Certifique-se de que mediu apenas o tempo real da ação."
                    )
                    
                # Se passou por todas as barreiras sem erros, salva no banco!
                else:
                    salvar_no_banco(nome_aluno.strip(), turma_ativa, l_banho, l_escova, l_total)
                    st.session_state.dados_enviados = True
                    st.success("Salvo!")
                    st.rerun()