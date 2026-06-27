import streamlit as st
import time
from app.frontend.abas_professor.Quiz_aba import renderizar_quiz_aluno # Atualização vem do Quiz
from app.backend.database import (
    verificar_turma_liberada, 
    verificar_escola_liberada,
    verificar_modo_aula, 
    verificar_aluno_matriculado,
    registrar_nota_quiz,
    buscar_ufs_cadastradas,
    buscar_municipios_por_uf,
    buscar_escolas_por_municipio,
    buscar_turmas_da_escola
)

from app.frontend.abas_professor.Calculadora_aba import renderizar_calculadora
from app.frontend.abas_professor.Funcoes_aba import renderizar_funcoes
from app.frontend.abas_professor.Financeiro_aba import renderizar_financeiro

st.set_page_config(page_title="Área do Aluno", page_icon="👨‍🎓")

# =====================================================================
# 🔏 VALIDAÇÕES DE ACESSO RIGOROSO
# =====================================================================
escola_ativa = verificar_escola_liberada()
turma_ativa = verificar_turma_liberada()

if turma_ativa == "FECHADO" or not escola_ativa:
    st.warning("⏳ A sala de aula interativa está fechada. Aguarde o professor liberar o acesso no projetor!")
    if st.button("🔄 Tentar Novamente"):
        st.rerun()
    st.stop()

# =====================================================================
# 🌎 LOGIN DO ALUNO (FILTROS EM CASCATA: UF -> MUNICIPIO -> ESCOLA)
# =====================================================================
if "aluno_autenticado" not in st.session_state:
    st.title("👋 Portal Interativo do Aluno")
    st.markdown("Preencha seus dados exatamente como estão na lista de chamada para entrar na sala.")
    st.divider()
    
    # [MODIFICAÇÃO PARA ESCALABILIDADE]: Cascata Nível 1 - Estado
    ufs_disponiveis = buscar_ufs_cadastradas()
    if not ufs_disponiveis:
        st.info("Nenhuma escola ativa no sistema ainda.")
        st.stop()

    uf_sel = st.selectbox("🌎 1. Selecione seu Estado:", ["Selecione..."] + ufs_disponiveis)
    
    if uf_sel != "Selecione...":
        # [MODIFICAÇÃO PARA ESCALABILIDADE]: Cascata Nível 2 - Município
        muns_disponiveis = buscar_municipios_por_uf(uf_sel)
        mun_sel = st.selectbox("🏙️ 2. Selecione seu Município:", ["Selecione..."] + muns_disponiveis)
        
        if mun_sel != "Selecione...":
            # [MODIFICAÇÃO PARA ESCALABILIDADE]: Cascata Nível 3 - Escola
            escolas_disponiveis = buscar_escolas_por_municipio(uf_sel, mun_sel)
            escola_sel = st.selectbox("🏫 3. Selecione sua Escola:", ["Selecione..."] + escolas_disponiveis)
            
            if escola_sel != "Selecione...":
                turmas_disponiveis = buscar_turmas_da_escola(escola_sel)
                turma_sel = st.selectbox("🎓 4. Selecione sua Turma:", ["Selecione..."] + turmas_disponiveis)
                
                if turma_sel != "Selecione...":
                    nome_digitado = st.text_input("👤 5. Digite seu nome (Primeiro e Segundo nome):")
                    
                    if st.button("Validar Identidade e Entrar"):
                        if escola_sel != escola_ativa or turma_sel != turma_ativa:
                            st.error(f"❌ Acesso Negado! A sala aberta agora é a **{turma_ativa}** na escola **{escola_ativa}**. Confirme sua turma e escola.")
                        else:
                            nome_limpo = nome_digitado.strip()
                            if len(nome_limpo.split()) < 2:
                                st.warning("⚠️ Digite pelo menos o primeiro e segundo nome.")
                            else:
                                matriculado = verificar_aluno_matriculado(nome_limpo, turma_sel, escola_sel)
                                if matriculado:
                                    st.success("✅ Identidade confirmada! Preparando a estação...")
                                    st.session_state.aluno_autenticado = True
                                    st.session_state.nome_aluno = nome_limpo
                                    st.session_state.escola_aluno = escola_sel
                                    st.session_state.turma_aluno = turma_sel
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error(f"❌ O nome '{nome_limpo}' não foi encontrado na lista da {turma_sel}. Verifique a grafia.")
    st.stop()

# =====================================================================
# 🎛️ CONTROLE REMOTO DA AULA
# =====================================================================
modo_aula = verificar_modo_aula()

st.sidebar.success(f"👤 Investigador: {st.session_state.nome_aluno}")
st.sidebar.info(f"🏫 Escola: {st.session_state.escola_aluno}")
st.sidebar.info(f"🎓 Turma: {st.session_state.turma_aluno}")

if st.sidebar.button("🔄 Sincronizar"):
    st.rerun()

if st.session_state.turma_aluno != turma_ativa or st.session_state.escola_aluno != escola_ativa:
    st.session_state.clear()
    st.warning("🔄 A turma ativa foi alterada pelo professor.")
    time.sleep(2)
    st.rerun()

# =====================================================================
# 🚀 RENDERIZAÇÃO DOS CENÁRIOS
# =====================================================================
if modo_aula == "FECHADO":
    st.info("🎯 Você está conectado com sucesso! Aguarde as instruções do professor.")
elif modo_aula == "CALCULADORA":
    st.title("📊 Estação de Coleta de Dados")
    st.session_state.nome_aluno_calc = st.session_state.nome_aluno
    st.session_state.escola_ativa_calc = st.session_state.escola_aluno
    st.session_state.turma_ativa_calc = st.session_state.turma_aluno
    renderizar_calculadora()
elif modo_aula == "FUNCOES":
    renderizar_funcoes()
elif modo_aula == "FINANCEIRO":
    renderizar_financeiro()
# Atualizada Novo Quiz
elif modo_aula == "QUIZ":
    st.title("🎮 Hora do Desafio: Game Quiz!")
    # Chama a sua função espetacular passando os dados do aluno!
    renderizar_quiz_aluno(
        nome_aluno=st.session_state.nome_aluno, 
        escola_atual=st.session_state.escola_aluno, 
        turma_atual=st.session_state.turma_aluno
    )