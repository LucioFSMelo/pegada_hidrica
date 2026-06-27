import streamlit as st
import pandas as pd
import time
import requests # <--- BIBLIOTECA PARA ACESSAR O IBGE


from app.backend.database import (
    cadastrar_professor_completo,
    login_professor_completo,
    buscar_escolas_do_professor,
    buscar_turmas_da_escola,
    importar_alunos_via_dataframe,
    atualizar_controle_aula
)

from app.frontend.Trilhas_Pedagogicas import (
    renderizar_trilha_matematica, renderizar_trilha_fisica,
    renderizar_trilha_portugues, renderizar_trilha_geografia,
    renderizar_trilha_ciencias
)

from app.frontend.abas_professor.Resultados_Quiz_aba import renderizar_aba_resultados_quiz

st.set_page_config(page_title="Central do Professor", page_icon="👨‍🏫", layout="wide")

# =====================================================================
# 🌐 FUNÇÃO DE BUSCA NO IBGE (MÁGICA DO DROPDOWN)
# =====================================================================
@st.cache_data(show_spinner=False)
def carregar_municipios_ibge(uf):
    """Busca a lista de municípios na API pública do IBGE baseada na UF."""
    try:
        url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
        resposta = requests.get(url, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            # Retorna apenas os nomes das cidades, em ordem alfabética
            return [cidade['nome'] for cidade in dados]
    except Exception:
        pass
    # Se der erro ou o IBGE estiver fora do ar, libera para o professor digitar
    return ["Digite o município..."]

# =====================================================================
# 🔐 SISTEMA DE LOGIN E CADASTRO
# =====================================================================
if "prof_logado" not in st.session_state:
    st.title("👨‍🏫 Central de Comando Multidisciplinar")
    st.write("Painel de gerenciamento escolar, orquestração de turmas e estações pedagógicas.")
    
    aba_login, aba_cadastro = st.tabs(["🔑 Login", "📝 Novo Cadastro"])
    
    with aba_login:
        with st.form("form_login"):
            email_login = st.text_input("E-mail:")
            senha_login = st.text_input("Senha:", type="password")
            submit_login = st.form_submit_button("Acessar Painel")
            
            if submit_login:
                if email_login.strip() and senha_login.strip():
                    resultado = login_professor_completo(email_login.strip(), senha_login.strip())
                    if resultado:
                        st.session_state.prof_logado = resultado[1] 
                        st.session_state.nome_prof = resultado[0]
                        st.session_state.disciplina_prof = resultado[2]
                        st.success(f"Autenticação bem-sucedida! Seja bem-vindo(a), Prof. {resultado[0]}.")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Credenciais não localizadas.")
                else:
                    st.warning("Preencha todos os campos.")
                    
    with aba_cadastro:
        # Removido o st.form para permitir a atualização em tempo real do Município
        nome_cad = st.text_input("Nome Completo:", key="cad_nome")
        email_cad = st.text_input("E-mail de Acesso:", key="cad_email")
        senha_cad = st.text_input("Defina uma Senha:", type="password", key="cad_senha")
        
        st.divider()
        st.markdown("#### 📚 Alocação de Componente Curricular")
        disciplinas = ["Matemática", "Física", "Língua Portuguesa", "Geografia", "Ciências"]
        disciplina_cad = st.selectbox("Sua disciplina:", disciplinas, key="cad_disc")
        
        st.markdown("#### 🌎 Localização de Atuação (Via IBGE)")
        lista_ufs = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
        
        col1, col2 = st.columns(2)
        with col1:
            uf_cad = st.selectbox("Estado (UF):", lista_ufs, index=16, key="cad_uf") # Padrão: PE
            
        with col2:
            # 🚀 MÁGICA: O sistema puxa automaticamente as cidades do estado selecionado!
            lista_municipios = carregar_municipios_ibge(uf_cad)
            
            # Se o IBGE falhar, ele exibe um text_input normal. Se funcionar, exibe a caixa de seleção.
            if lista_municipios[0] == "Digite o município...":
                municipio_cad = st.text_input("Município:", key="cad_mun_texto")
            else:
                municipio_cad = st.selectbox("Município:", lista_municipios, key="cad_mun_select")
        
        st.markdown("#### 🏫 Lotação Escolar")
        escola1_cad = st.text_input("Nome da Escola Principal (Obrigatório):", key="cad_escola1")
        escola2_cad = st.text_input("Nome da Segunda Escola (Opcional):", key="cad_escola2")
        
        # Botão normal em vez de botão de formulário
        if st.button("Finalizar Cadastro de Perfil"):
            if nome_cad and email_cad and senha_cad and escola1_cad and municipio_cad:
                escolas = [escola1_cad, escola2_cad]
                sucesso, mensagem = cadastrar_professor_completo(
                    nome_cad.strip(), email_cad.strip(), senha_cad.strip(), disciplina_cad, uf_cad, municipio_cad, escolas
                )
                if sucesso:
                    st.success(mensagem + " Alterne para a aba de Login.")
                else:
                    st.error(mensagem)
            else:
                st.warning("Preencha Nome, Email, Senha, Município e a Escola Principal.")
    st.stop()


# =====================================================================
# 🎛️ PAINEL DO PROFESSOR LOGADO
# =====================================================================
st.sidebar.success(f"👤 Docente: {st.session_state.nome_prof}")
st.sidebar.info(f"📚 Trilha Ativa: {st.session_state.disciplina_prof}")

if st.sidebar.button("🚪 Encerrar Sessão"):
    st.session_state.clear()
    st.rerun()

st.title(f"Painel de Orquestração - {st.session_state.disciplina_prof}")

aba_controle, aba_alunos, aba_resultados, aba_quiz = st.tabs([
    "🎛️ Controle Remoto", "📥 Importar Planilha", "🏆 Laboratório", "📊 Resultados do Quiz"
])

escolas_do_prof = buscar_escolas_do_professor(st.session_state.prof_logado)

with aba_alunos:
    st.subheader("📥 Carga em Lote da Lista Oficial")
    if escolas_do_prof:
        escola_selecionada = st.selectbox("Selecione a Escola:", escolas_do_prof, key="import_escola")
        arquivo_upload = st.file_uploader("Upload do Arquivo (.xlsx ou .csv):", type=["xlsx", "csv"])
        
        if arquivo_upload is not None:
            if st.button("🚀 Executar Importação"):
                try:
                    if arquivo_upload.name.endswith('.csv'):
                        df = pd.read_csv(arquivo_upload)
                        sucesso, msg = importar_alunos_via_dataframe(df, escola_selecionada)
                    else:
                        xls = pd.read_excel(arquivo_upload, sheet_name=None)
                        dfs_processados = []
                        for nome_aba, df_aba in xls.items():
                            colunas_lower = [str(c).strip().lower() for c in df_aba.columns]
                            if not any('turma' in c for c in colunas_lower):
                                df_aba['turma'] = str(nome_aba).strip()
                            dfs_processados.append(df_aba)
                        df_final = pd.concat(dfs_processados, ignore_index=True)
                        sucesso, msg = importar_alunos_via_dataframe(df_final, escola_selecionada)
                        
                    if sucesso:
                        st.success(msg)
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(msg)
                except Exception as e:
                    st.error(f"Incompatibilidade estrutural. Detalhes: {e}")

with aba_controle:
    st.subheader("📡 Controle Remoto")
    if escolas_do_prof:
        escola_aula = st.selectbox("1. Escola Ativa:", escolas_do_prof, key="ctrl_escola")
        turmas_disponiveis = buscar_turmas_da_escola(escola_aula)
        
        if turmas_disponiveis:
            turma_aula = st.selectbox("2. Turma Ativa:", ["FECHADO"] + turmas_disponiveis, key="ctrl_turma")
            modo_aula = st.radio("3. Cenário para os Alunos:", ["FECHADO", "CALCULADORA", "FUNCOES", "FINANCEIRO", "QUIZ"], horizontal=True)
            
            if st.button("📡 Emitir Sinal para as Telas"):
                atualizar_controle_aula(turma_aula, escola_aula, modo_aula)
                if turma_aula == "FECHADO":
                    st.warning("Comando: Acesso trancado aos alunos.")
                else:
                    st.success(f"Sinal propagado! Estudantes direcionados para: {modo_aula}.")

with aba_resultados:
    d = st.session_state.disciplina_prof
    if d == "Matemática": renderizar_trilha_matematica()
    elif d == "Física": renderizar_trilha_fisica()
    elif d == "Língua Portuguesa": renderizar_trilha_portugues()
    elif d == "Geografia": renderizar_trilha_geografia()
    elif d in ["Ciências", "Biologia", "Química"]: renderizar_trilha_ciencias()

# 👇 2. INCLUÍMOS O BLOCO DO QUIZ AQUI NO FINAL
with aba_quiz:
    if escolas_do_prof:
        col1, col2 = st.columns(2)
        with col1:
            # Filtro para escolher de qual escola quer ver o resultado
            escola_quiz = st.selectbox("Escola para análise:", escolas_do_prof, key="quiz_escola_sel")
        with col2:
            # Filtro para escolher a turma
            turmas_quiz = buscar_turmas_da_escola(escola_quiz)
            turma_quiz = st.selectbox("Turma para análise:", turmas_quiz if turmas_quiz else ["Nenhuma"], key="quiz_turma_sel")
        
        st.divider()
        
        if turmas_quiz:
            # Chama a função que criamos passando a escola e turma que você selecionou agora
            renderizar_aba_resultados_quiz(escola_atual=escola_quiz, turma_atual=turma_quiz)
        else:
            st.info("Importe alunos para esta escola para começar a captar resultados.")
    else:
        st.warning("Você ainda não tem escolas cadastradas.")

