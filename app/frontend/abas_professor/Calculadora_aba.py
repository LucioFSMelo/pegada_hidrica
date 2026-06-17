import streamlit as st
from app.backend.calculator import calcular_pegada
from app.backend.database import salvar_no_banco, verificar_turma_liberada

def renderizar_calculadora():
    st.subheader("📊 Estação de Coleta: Pegada Hídrica")
    turma_ativa = verificar_turma_liberada()
    
    if turma_ativa == "FECHADO":
        st.error("⛔ A calculadora está travada. Ative ou libere uma turma na aba 'Gerenciar Gincana' primeiro!")
    else:
        st.success(f"🔓 Pronto para coletar dados da turma: **{turma_ativa}**")
        
        if "dados_enviados" not in st.session_state:
            st.session_state.dados_enviados = False
            
        nome_aluno = st.text_input("Digite o primeiro nome do aluno:")
        
        st.divider()
        t_banho = st.slider("Tempo de banho diário (minutos):", 1, 30, 10, key="calc_banho")
        c_fechado = st.radio("Fecha o chuveiro ao se ensaboar?", ("Sim, eu fecho! 🟢", "Não, deixo ligado! 🔴"), key="calc_chuveiro")
        
        t_escova = st.slider("Minutos gastando escovando os dentes por dia:", 1, 10, 4, key="calc_escova")
        t_fechada = st.radio("Fecha a torneira ao escovar os dentes?", ("Sim, sempre fecho! 🟢", "Não, fica aberta! 🔴"), key="calc_torneira")
        
        l_banho, l_escova, l_total = calcular_pegada(t_banho, c_fechado, t_escova, t_fechada)
        
        st.markdown("##### Resultado do Aluno:")
        col_b, col_e, col_t = st.columns(3)
        col_b.metric("Banho", f"{l_banho:.1f} L")
        col_e.metric("Escovação (10%)", f"{l_escova:.1f} L")
        col_t.metric("Total Diário", f"{l_total:.1f} L")
        
        if st.session_state.dados_enviados:
            st.success("✅ Dados gravados com sucesso no banco!")
            if st.button("🔄 Coletar dados do próximo aluno"):
                st.session_state.dados_enviados = False
                st.rerun()
        else:
            if st.button("💾 Salvar Registro no Banco de Dados", use_container_width=True):
                if nome_aluno.strip() == "":
                    st.error("Por favor, preencha o nome do aluno.")
                else:
                    salvar_no_banco(nome_aluno, turma_ativa, l_banho, l_escova, l_total)
                    st.session_state.dados_enviados = True
                    st.success("Salvo!")
                    st.rerun()