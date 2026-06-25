import streamlit as st
import time
from app.backend.database import (
    verificar_turma_liberada, 
    verificar_modo_aula, 
    registrar_nota_quiz
)

# 🔄 IMPORTAÇÃO INTEGRADA DE TODAS AS ABAS DO ECOSSISTEMA
from app.frontend.abas_professor.Calculadora_aba import renderizar_calculadora
from app.frontend.abas_professor.Funcoes_aba import renderizar_funcoes
from app.frontend.abas_professor.Financeiro_aba import renderizar_financeiro

st.set_page_config(page_title="Área do Aluno", page_icon="👨‍🎓")

# =====================================================================
# 🔏 VALIDAÇÕES DE ACESSO INDISPENSÁVEIS (PORTAL DE ENTRADA)
# =====================================================================

# 1. Checa se o professor abriu e destrancou a turma no sistema
turma_atual = verificar_turma_liberada()

if turma_atual == "FECHADO":
    st.warning("⏳ A aula ainda não começou ou está pausada. Aguarde o professor liberar o acesso no painel dele.")
    if st.button("🔄 Atualizar Tela"):
        st.rerun()
    st.stop() # Bloqueia qualquer execução posterior

# 2. Identificação do Aluno (Necessário para vincular Notas do Quiz e Consumo)
if "nome_aluno" not in st.session_state:
    st.title("👋 Bem-vindo à Gincana Hídrica!")
    nome = st.text_input("Por favor, digite o seu nome completo para entrar na sala virtual:")
    if st.button("Entrar na Aula"):
        if nome.strip():
            st.session_state.nome_aluno = nome.strip()
            st.rerun()
        else:
            st.error("⚠️ Identificação obrigatória. Digite seu nome para continuar.")
    st.stop()

# =====================================================================
# 🎛️ CONTROLE REMOTO DA AULA (LEITURA DINÂMICA DO BANCO)
# =====================================================================
modo_aula = verificar_modo_aula()

# Interface Lateral de Identificação do Aluno Investigador
st.sidebar.success(f"👤 Aluno: {st.session_state.nome_aluno}")
st.sidebar.info(f"🏫 Turma Ativa: {turma_atual}")

# Botão de Sincronização Manual (Evita deslogar e puxa comandos do professor)
if st.sidebar.button("🔄 Sincronizar Painel"):
    st.rerun()

# =====================================================================
# 🚀 RENDERIZAÇÃO DOS CENÁRIOS DE AULA (ORQUESTRAÇÃO COMPLETA)
# =====================================================================

# Cenário 0: Sala aberta, mas nenhuma atividade selecionada pelo docente
if modo_aula == "FECHADO":
    st.info("🎯 O professor liberou a entrada na sala! Aguarde as instruções para saber qual estação iniciaremos.")

# Cenário 1: Estação da Calculadora de Pegada Hídrica
elif modo_aula == "CALCULADORA":
    st.title("📊 Coleta de Dados Hídricos")
    st.write("Preencha seus dados de consumo abaixo para enviar ao Placar Geral:")
    # Passa o nome do aluno da sessão para preenchimento automático na calculadora
    st.session_state.nome_aluno_calc = st.session_state.nome_aluno
    renderizar_calculadora()
    
# Cenário 2: Estação de Probabilidade e BNCC
elif modo_aula == "FUNCOES":
    renderizar_funcoes()
    
# Cenário 3: Estação de Consciência Financeira (Metros Cúbicos)
elif modo_aula == "FINANCEIRO":
    renderizar_financeiro()
    
# Cenário 4: Gincana Competitiva - Game Quiz Interativo
elif modo_aula == "QUIZ":
    st.title("🎮 Hora do Desafio: Game Quiz!")
    st.write("Responda com máxima atenção! Acertos valem **+3 pontos**. Erros removem **-1 ponto**.")
    st.divider()
    
    # Armazena localmente o estado de envio do Quiz para não resetar no meio das respostas
    if "quiz_enviado" not in st.session_state:
        st.session_state.quiz_enviado = False
        
    if st.session_state.quiz_enviated:
        st.success("🎉 Suas respostas foram computadas! Verifique o Placar Geral no projetor do professor.")
        if st.button("🔄 Responder Novamente (Caso o professor permita)"):
            st.session_state.quiz_enviado = False
            st.rerun()
    else:
        # Formulário Estruturado do Quiz
        with st.form("quiz_aluno_form"):
            st.markdown("##### 1. Qual o equivalente em litros para $1 m^3$ de água tratada?")
            r1 = st.radio("Selecione a alternativa correta:", ["10 Litros", "100 Litros", "1.000 Litros", "10.000 Litros"], key="q1")
            
            st.markdown("##### 2. Qual hábito consome menos água de forma eficiente de acordo com as missões?")
            r2 = st.radio("Selecione a alternativa correta:", [
                "Deixar a torneira aberta enquanto esfrega os dentes.",
                "Fechar o chuveiro enquanto se ensaboa no banho.",
                "Lavar a calçada usando a mangueira como vassoura.",
                "Tomar banhos de 30 minutos todos os dias."
            ], key="q2")
            
            st.markdown("##### 3. Na fórmula de Probabilidade $P(A) = n(A) / n(\Omega)$, o que representa o $n(\Omega)$?")
            r3 = st.radio("Selecione a alternativa correta:", [
                "O número de casos favoráveis ao meu sorteio.",
                "O consumo total da escola inteira.",
                "O tamanho total do Espaço Amostral (Todos os resultados possíveis).",
                "A quantidade de água desperdiçada."
            ], key="q3")
            
            # Botão de envio do formulário do Quiz
            enviar_respostas = st.form_submit_button("🚀 Enviar Minhas Respostas", use_container_width=True)
            
            if enviar_respostas:
                # Sistema Gabarito de Pontuação Pedagógica
                pontos = 0
                
                # Pergunta 1: Certo = 1.000 Litros
                if r1 == "1.000 Litros": pontos += 3
                else: pontos -= 1
                    
                # Pergunta 2: Certo = Fechar o chuveiro...
                if r2 == "Fechar o chuveiro enquanto se ensaboa no banho.": pontos += 3
                else: pontos -= 1
                    
                # Pergunta 3: Certo = O tamanho total do Espaço Amostral...
                if r3 == "O tamanho total do Espaço Amostral (Todos os resultados possíveis).": pontos += 3
                else: pontos -= 1
                
                # Garante que a pontuação do aluno não fique negativa em caso de muitos erros
                pontuacao_final = max(0, pontos)
                
                # 💾 GRAVAÇÃO DIRETA NO BANCO DE DADOS
                registrar_nota_quiz(turma_atual, st.session_state.nome_aluno, pontuacao_final)
                
                st.session_state.quiz_enviado = True
                st.rerun()