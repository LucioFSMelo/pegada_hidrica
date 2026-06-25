import sys
import os
import streamlit as st

# =====================================================================
# 🗃️ BLINDAGEM DE CONFIGURAÇÃO DE CAMINHO ABSOLUTO
# =====================================================================
# Garante que o Python encontre os módulos do projeto independente de onde o app foi iniciado.
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__)) 
PASTA_FRONTEND = os.path.dirname(DIRETORIO_ATUAL)            
PASTA_APP = os.path.dirname(PASTA_FRONTEND)                  
RAIZ_PROJETO = os.path.dirname(PASTA_APP)                    

if RAIZ_PROJETO not in sys.path:
    sys.path.insert(0, RAIZ_PROJETO)

# --- IMPORTS DO BACKEND (Controle de Banco de Dados e Segurança) ---
from app.backend.database import (
    login_ou_cadastro_professor, 
    adicionar_turma, 
    buscar_turmas_do_professor, 
    definir_turma_liberada, 
    verificar_turma_liberada, 
    apagar_dados_por_turma,
    verificar_email_professor,
    redefinir_senha_professor,
    deletar_turma_completa,
    definir_modo_aula,       # ✨ NOVO: Envia o comando da tela atual para o banco
    verificar_modo_aula,     # ✨ NOVO: Lê o status da tela ativa
    obter_ranking_quiz       # ✨ NOVO: Puxa as pontuações do quiz (+3/-1) ordenadas
)

# --- IMPORTS EXCLUSIVOS DAS ABAS DO PROFESSOR (Interface Modular) ---
from app.frontend.abas_professor.Calculadora_aba import renderizar_calculadora
from app.frontend.abas_professor.Ranking_aba import renderizar_ranking
from app.frontend.abas_professor.Estatistica_aba import renderizar_estatistica
from app.frontend.abas_professor.Funcoes_aba import renderizar_funcoes
from app.frontend.abas_professor.Financeiro_aba import renderizar_financeiro
from app.frontend.abas_professor.Dicas_aba import renderizar_dicas

# Configuração da Página do Streamlit
st.set_page_config(page_title="Painel do Professor", page_icon="👨‍🏫", layout="wide")

st.title("👨‍🏫 Central de Comando do Professor")

# =====================================================================
# 🔐 BLINKAGEM E CONTROLE DE ACESSO (LOGIN / CADASTRO)
# =====================================================================
if "prof_logado" not in st.session_state:
    st.markdown("### 🔐 Área Restrita do Orientador")
    
    usuario = st.text_input("Usuário (Login):").strip()
    senha = st.text_input("Senha:", type="password").strip()
    
    # Campo explicativo de e-mail para blindar novos cadastros
    email_cadastro = st.text_input(
        "E-mail (Obrigatório apenas para novos cadastros):", 
        help="Caso você já tenha uma conta, deixe em branco. Se for seu primeiro acesso, digite seu e-mail para recuperação de senha offline."
    ).strip()
    
    if st.button("Acessar / Criar Conta", use_container_width=True):
        if usuario == "" or senha == "":
            st.error("⚠️ Preencha usuário e senha.")
        else:
            # Envia os dados para autenticação ou cadastro seguro usando SHA-256 no banco
            status = login_ou_cadastro_professor(usuario, senha, email_cadastro)
            
            if status == "SENHA_INCORRETA": 
                st.error("❌ Senha incorreta!")
            elif status == "CAMPOS_VAZIOS": 
                st.error("⚠️ Preencha usuário e senha.")
            else:
                st.session_state.prof_logado = usuario
                st.rerun()
                
    # --- GAVETA DE RECUPERAÇÃO DE SENHA POR E-MAIL OFFLINE ---
    st.markdown("---")
    with st.expander("🔑 Esqueci minha senha (Validação Local)"):
        st.caption("Esqueceu suas credenciais? Digite seu usuário e e-mail cadastrado para criar uma nova senha na hora, sem precisar de internet.")
        
        rec_usuario = st.text_input("Digite seu Usuário:", key="rec_user").strip()
        rec_email = st.text_input("Digite seu E-mail Cadastrado:", key="rec_mail").strip()
        
        if st.button("🔓 Verificar Identidade", use_container_width=True):
            if rec_usuario == "" or rec_email == "":
                st.error("Por favor, preencha os dois campos para validação.")
            elif verificar_email_professor(rec_usuario, rec_email):
                st.session_state["autorizado_redefinir"] = rec_usuario.lower()
                st.success("🎯 Identidade confirmada com sucesso! Crie sua nova senha no formulário abaixo.")
            else:
                st.error("❌ Usuário ou E-mail incorretos. Tente novamente.")
                
        # Exibe o formulário de redefinição se o e-mail bater com o registro local
        if "autorizado_redefinir" in st.session_state and st.session_state["autorizado_redefinir"] == rec_usuario.lower():
            st.markdown("#### Cadastrar Nova Senha")
            nova_senha = st.text_input("Digite a nova senha:", type="password", key="n_pass1")
            nova_senha_conf = st.text_input("Confirme a nova senha:", type="password", key="n_pass2")
            
            if st.button("💾 Salvar Nova Senha", use_container_width=True):
                if len(nova_senha) < 4:
                    st.warning("Escolha uma senha com pelo menos 4 caracteres.")
                elif nova_senha != nova_senha_conf:
                    st.error("⚠️ As senhas digitadas não coincidem.")
                else:
                    if redefinir_senha_professor(rec_usuario, nova_senha):
                        st.success("✅ Senha atualizada! Você já pode fechar este menu e fazer o login.")
                        del st.session_state["autorizado_redefinir"]
                    else:
                        st.error("Erro interno ao atualizar o banco de dados.")

else:
    # =====================================================================
    # 💻 INTERFACE PRINCIPAL DO PAINEL DO PROFESSOR (LOGADO)
    # =====================================================================
    st.sidebar.success(f"Sessão Ativa: {st.session_state.prof_logado}")
    if st.sidebar.button("🚪 Sair do Painel"):
        del st.session_state.prof_logado
        st.rerun()

    # ✨ ATUALIZADO: Criação das abas incluindo a nova central do "Game Quiz"
    aba_gerenciar, aba_calc, aba_rank, aba_estat, aba_func, aba_finan, aba_dicas, aba_quiz = st.tabs([
        "⚙️ Gerenciar Gincana", 
        "📊 Calculadora", 
        "🏆 Ranking Consumo", 
        "📈 Estatística", 
        "🧮 Funções", 
        "💰 Financeiro",
        "💡 Dicas e Missões",
        "🎮 Game Quiz" # Nova aba de monitoramento ao vivo do Quiz
    ])

    # -----------------------------------------------------------------
    # ⚙️ ABA: GERENCIAR GINCANA (Orquestração e Cadeados)
    # -----------------------------------------------------------------
    with aba_gerenciar:
        st.subheader("⚙️ Configurações Gerais e Direção de Aula")
        col_c, col_l = st.columns(2)
        
        with col_c:
            st.markdown("#### 📝 Cadastrar Turma")
            nova_turma = st.text_input("Nome (Ex: 6º ANO B):").strip()
            if st.button("Cadastrar", use_container_width=True):
                if nova_turma and adicionar_turma(st.session_state.prof_logado, nova_turma):
                    st.success("Cadastrada!")
                    st.rerun()
                else: 
                    st.error("Turma já existente ou campo vazio.")
                    
        with col_l:
            st.markdown("#### 🔓 Liberar e Orquestrar Aplicativo")
            turmas_do_prof = buscar_turmas_do_professor(st.session_state.prof_logado)
            
            # Mostra o status global do sistema para o professor saber o que está ativo
            col_status1, col_status2 = st.columns(2)
            with col_status1:
                st.metric("Turma Liberada:", verificar_turma_liberada())
            with col_status2:
                st.metric("Atividade Ativa:", verificar_modo_aula())
            
            if turmas_do_prof:
                t_sel = st.selectbox("Selecione a turma para gerenciar:", turmas_do_prof)
                
                if st.button("🟢 ABRIR Acesso à Turma", use_container_width=True):
                    definir_turma_liberada(t_sel)
                    st.rerun()
                    
                if st.button("🔴 FECHAR Acesso Geral", use_container_width=True):
                    definir_turma_liberada("FECHADO")
                    definir_modo_aula("FECHADO") # Bloqueia também as atividades dos alunos
                    st.rerun()
                
                st.markdown("---")
                st.markdown("#### 📱 Diretor de Aula (Mudar Tela dos Alunos)")
                st.caption("Escolha qual funcionalidade aparecerá instantaneamente nos dispositivos dos alunos.")
                
                # Seletor dinâmico que manipula o arquivo do aluno remoto
                tela_sel = st.selectbox(
                    "Selecione a Atividade:", 
                    ["📊 Calculadora", "🧮 Funções", "💰 Financeiro", "🎮 Quiz"]
                )
                
                # Dicionário de mapeamento para constantes do Banco de Dados
                mapa_modos = {
                    "📊 Calculadora": "CALCULADORA",
                    "🧮 Funções": "FUNCOES",
                    "💰 Financeiro": "FINANCEIRO",
                    "🎮 Quiz": "QUIZ"
                }
                
                if st.button("🚀 Enviar Atividade e Forçar Mudança de Tela", use_container_width=True):
                    modo_convertido = mapa_modos[tela_sel]
                    definir_modo_aula(modo_convertido)
                    st.success(f"Sucesso! Todos os computadores da turma mudarão para: {tela_sel}")
                    st.rerun()
                
                st.markdown("---")
                st.markdown("#### ⚠️ Perigo / Limpeza de Dados")
                
                if st.button(f"🗑️ Zerar Banco de Consumo do {t_sel}", use_container_width=True):
                    apagar_dados_por_turma(t_sel)
                    st.success("Dados de consumo limpos!")
                
                # Botão de exclusão definitiva em cascata para virada de ano letivo
                if st.button(f"💥 EXCLUIR DEFINITIVAMENTE o {t_sel}", use_container_width=True):
                    if deletar_turma_completa(st.session_state.prof_logado, t_sel):
                        st.success(f"A turma '{t_sel}' e todos os consumos dela foram completamente removidos.")
                        st.rerun()
                    else:
                        st.error("Erro interno ao tentar remover a turma do banco de dados.")

    # -----------------------------------------------------------------
    # INJEÇÃO DOS MÓDULOS PADRÃO DO PROFESSOR
    # -----------------------------------------------------------------
    with aba_calc:
        renderizar_calculadora()

    with aba_rank:
        renderizar_ranking()

    with aba_estat:
        renderizar_estatistica()

    with aba_func:
        renderizar_funcoes()

    with aba_finan:
        renderizar_financeiro()

    with aba_dicas:
        renderizar_dicas()

    # -----------------------------------------------------------------
    # 🎮 ABA: GAME QUIZ (Painel do Pódio e Tabela Decrescente)
    # -----------------------------------------------------------------
    with aba_quiz:
        st.header("🎮 Central do Quiz e Gamificação")
        st.markdown("Acompanhe as respostas e o ranking competitivo dos alunos em tempo real.")
        
        turma_atual = verificar_turma_liberada()
        
        if turma_atual == "FECHADO":
            st.warning("⚠️ Abra o acesso de alguma turma na aba '⚙️ Gerenciar Gincana' para monitorar o Quiz.")
        else:
            st.info(f"Visualizando dados em tempo real da turma ativa: **{turma_atual}**")
            
            # Botão manual para o professor atualizar as notas à medida que os alunos concluem
            if st.button("🔄 Atualizar Classificação Ao Vivo", use_container_width=True):
                st.rerun()
                
            # Coleta as pontuações calculadas sob a regra (+3 por acerto / -1 por erro)
            df_quiz = obter_ranking_quiz(turma_atual)
            
            if df_quiz.empty:
                st.write("⏳ Nenhum aluno finalizou o Quiz nesta rodada ainda. Aguarde as respostas!")
            else:
                st.markdown("### 🏆 Pódio dos Campeões")
                
                # Criação das três colunas visuais para destaque do Top 3
                col1, col2, col3 = st.columns(3)
                
                # 🥇 1º Lugar
                if len(df_quiz) >= 1:
                    aluno1 = df_quiz.iloc[0]
                    col1.metric("🥇 1º Lugar", f"👤 {aluno1['nome_aluno']}", f"{aluno1['pontuacao']} pts")
                
                # 🥈 2º Lugar
                if len(df_quiz) >= 2:
                    aluno2 = df_quiz.iloc[1]
                    col2.metric("🥈 2º Lugar", f"👤 {aluno2['nome_aluno']}", f"{aluno2['pontuacao']} pts")
                
                # 🥉 3º Lugar
                if len(df_quiz) >= 3:
                    aluno3 = df_quiz.iloc[2]
                    col3.metric("🥉 3º Lugar", f"👤 {aluno3['nome_aluno']}", f"{aluno3['pontuacao']} pts")
                
                st.markdown("---")
                st.markdown("#### 📋 Classificação Geral (Ordem Decrescente)")
                
                # Exibição limpa da tabela de notas ocultando o índice padrão do Pandas
                st.dataframe(
                    df_quiz, 
                    use_container_width=True,
                    column_config={
                        "nome_aluno": "Nome do Aluno (Detetive)",
                        "pontuacao": st.column_config.NumberColumn("Pontuação Conquistada", format="%d pontos")
                    },
                    hide_index=True
                )