import streamlit as st
from app.backend.calculator import calcular_pegada, TURMAS_OFICIAIS
from app.backend.database import salvar_no_banco

def renderizar_aba_calculadora():
    st.header("Análise de Hábitos Individuais")
    
    nome_aluno = st.text_input("Digite seu primeiro nome (e sobrenome se quiser):")
    turma_aluno = st.selectbox("Selecione sua turma:", TURMAS_OFICIAIS)
    
    st.divider()
    
    tempo_banho = st.slider("Quanto tempo dura o seu banho diariamente? (minutos)", 1, 30, 10)
    chuveiro_fechado = st.radio("Você fecha o chuveiro enquanto se ensaboa?", ("Sim, eu fecho! 🟢", "Não, deixo ligado o tempo todo! 🔴"))
    
    tempo_escovacao = st.slider("Quantos minutos no total você passa escovando os dentes por dia?", 1, 10, 4)
    torneira_escovacao = st.radio("Você fecha a torneira enquanto escova os dentes?", ("Sim, sempre fecho! 🟢", "Não, fica aberta! 🔴"))

    # Executa a regra vinda do backend
    litros_banho, litros_escovacao, litros_total = calcular_pegada(tempo_banho, chuveiro_fechado, tempo_escovacao, torneira_escovacao)

    st.subheader("🕵️‍♂️ Seu Resultado")
    col1, col2 = st.columns(2)
    col1.metric("Gasto no Banho", f"{litros_banho:.1f} L")
    col2.metric("Gasto na Escovação", f"{litros_escovacao:.1f} L")
    st.info(f"**Consumo direto estimado: {litros_total:.1f} litros por dia.**")

    if st.session_state.dados_enviados:
        st.success(f"🎉 Seus dados já foram computados, {nome_aluno}! Vá até a aba do Ranking.")
        if st.button("🔄 Enviar novos dados (Corrigir digitação)"):
            st.session_state.dados_enviados = False
            st.rerun()
    else:
        if st.button("💾 Enviar meus dados para o Banco de Dados"):
            if nome_aluno.strip() == "":
                st.error("⚠️ Por favor, digite seu nome antes de enviar!")
            else:
                salvar_no_banco(nome_aluno.strip(), turma_aluno, litros_banho, litros_escovacao, litros_total)
                st.session_state.dados_enviados = True
                st.success(f"✅ Sucesso! Os dados de {nome_aluno} foram salvos.")
                st.rerun()