import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import sqlite3

# Configuração da página
st.set_page_config(
    page_title="Detetives da Água - Competição Hídrica",
    page_icon="💧",
    layout="centered"
)

# --- FUNÇÕES DO BANCO DE DADOS (SQLITE) ---
DB_NAME = "banco_pegada_hidrica.db"

def inicializar_banco():
    """Cria a tabela no banco de dados se ela ainda não existir."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consumo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turma TEXT NOT NULL,
            gasto_banho REAL,
            gasto_escovacao REAL,
            gasto_total REAL
        )
    """)
    conn.commit()
    conn.close()

def salvar_no_banco(nome, turma, banho, escovacao, total):
    """Insere um novo registro de aluno no banco SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO consumo (nome, turma, gasto_banho, gasto_escovacao, gasto_total)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, turma, banho, escovacao, total))
    conn.commit()
    conn.close()

def ler_todos_dados():
    """Busca todos os registros salvos e retorna um DataFrame do Pandas."""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM consumo", conn)
    conn.close()
    return df

def apagar_banco():
    """Apaga todos os registros para reiniciar a gincana."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS consumo")
    conn.commit()
    conn.close()
    inicializar_banco()

# Inicializa o banco de dados ao rodar o app
inicializar_banco()

# --- LISTA OFICIAL DE TURMAS ---
TURMAS_OFICIAIS = ["8º A", "8º B", "8º C", "9º A", "9º B", "9º C"]

# --- CONTROLE DE CLIQUE ÚNICO (SESSION STATE) ---
# Se a variável 'dados_enviados' não existir nesta sessão, nós a iniciamos como Falsa
if "dados_enviados" not in st.session_state:
    st.session_state.dados_enviados = False

# --- INTERFACE DO USUÁRIO (STREAMLIT) ---

st.title("💧 Semana do Meio Ambiente: Pegada Hídrica")
st.markdown("""
**8º e 9º anos juntos contra o desperdício!** Calcule sua pegada, envie para o banco de dados e ajude sua turma na gincana!
""")

# Taxas de vazão padrão
VAZAO_CHUVEIRO = 15
VAZAO_TORNEIRA_PIA = 9

# Abas de navegação
aba1, aba2, aba3 = st.tabs(["📊 Minha Pegada Hídrica", "🏆 Ranking e Pódio", "🚀 Simulador Coletivo"])

# --- ABA 1: CALCULADORA INDIVIDUAL ---
with aba1:
    st.header("Análise de Hábitos Individuais")
    
    nome_aluno = st.text_input("Digite seu primeiro nome (e sobrenome se quiser):")
    turma_aluno = st.selectbox("Selecione sua turma:", TURMAS_OFICIAIS)
    
    st.divider()
    
    tempo_banho = st.slider("Quanto tempo dura o seu banho diariamente? (minutos)", 1, 30, 10)
    chuveiro_fechado = st.radio(
        "Você fecha o chuveiro enquanto se ensaboa?",
        ("Sim, eu fecho! 🟢", "Não, deixo ligado o tempo todo! 🔴")
    )
    
    tempo_escovacao = st.slider("Quantos minutos no total você passa escovando os dentes por dia?", 1, 10, 4)
    torneira_escovacao = st.radio(
        "Você fecha a torneira enquanto escova os dentes?",
        ("Sim, sempre fecho! 🟢", "Não, fica aberta! 🔴")
    )

    # Lógica de Cálculos matemáticos
    if "Sim" in chuveiro_fechado:
        tempo_chuveiro_ligado = tempo_banho / 2
    else:
        tempo_chuveiro_ligado = tempo_banho
    litros_banho = tempo_chuveiro_ligado * VAZAO_CHUVEIRO

    if "Sim" in torneira_escovacao:
        litros_escovacao = 0.5 * VAZAO_TORNEIRA_PIA
    else:
        litros_escovacao = tempo_escovacao * VAZAO_TORNEIRA_PIA

    litros_total = litros_banho + litros_escovacao

    st.subheader("🕵️‍♂️ Seu Resultado")
    col1, col2 = st.columns(2)
    col1.metric("Gasto no Banho", f"{litros_banho:.1f} L")
    col2.metric("Gasto na Escovação", f"{litros_escovacao:.1f} L")
    st.info(f"**Consumo direto estimado: {litros_total:.1f} litros por dia.**")

    # Modificado aqui: Se o aluno já enviou, desabilitamos o botão para evitar clique duplo
    if st.session_state.dados_enviados:
        st.success(f"🎉 Seus dados já foram computados, {nome_aluno}! Vá até a aba do Ranking para ver o resultado.")
        if st.button("🔄 Enviar novos dados (Corrigir digitação)"):
            st.session_state.dados_enviados = False
            st.rerun()
    else:
        if st.button("💾 Enviar meus dados para o Banco de Dados"):
            if nome_aluno.strip() == "":
                st.error("⚠️ Por favor, digite seu nome antes de enviar!")
            else:
                salvar_no_banco(nome_aluno.strip(), turma_aluno, litros_banho, litros_escovacao, litros_total)
                st.session_state.dados_enviados = True # Ativa a trava de segurança contra cliques múltiplos
                st.success(f"✅ Sucesso! Os dados de {nome_aluno} foram guardados no banco SQLite.")
                st.rerun()

# --- ABA 2: RANKING, PÓDIO E GRÁFICOS ---
with aba2:
    df_geral = ler_todos_dados()
    
    if df_geral.empty:
        st.warning("📥 O banco de dados SQLite está vazio. Aguardando o primeiro registro dos estudantes!")
    else:
        st.write(f"📊 **Total de participantes registrados no banco:** {len(df_geral)} alunos.")
        
        # 👑 ELEIÇÃO DOS ALUNOS MAIS ECONÔMICOS
        st.subheader("👑 Os Campeões da Economia (Pódio por Turma)")
        st.markdown("O aluno de cada turma que registrou o **menor consumo diário de água**:")
        
        st.markdown("#### **8º Anos**")
        col8_a, col8_b, col8_c = st.columns(3)
        for t, col in zip(["8º A", "8º B", "8º C"], [col8_a, col8_b, col8_c]):
            df_turma = df_geral[df_geral["turma"] == t]
            with col:
                st.markdown(f"**{t}**")
                if df_turma.empty:
                    st.caption("Sem registros")
                else:
                    campeao = df_turma.loc[df_turma["gasto_total"].idxmin()]
                    st.success(f"🥇 **{campeao['nome']}**\n\n**{campeao['gasto_total']:.1f} L/dia**")

        st.markdown("#### **9º Anos**")
        col9_a, col9_b, col9_c = st.columns(3)
        for t, col in zip(["9º A", "9º B", "9º C"], [col9_a, col9_b, col9_c]):
            df_turma = df_geral[df_geral["turma"] == t]
            with col:
                st.markdown(f"**{t}**")
                if df_turma.empty:
                    st.caption("Sem registros")
                else:
                    campeao = df_turma.loc[df_turma["gasto_total"].idxmin()]
                    st.success(f"🥇 **{campeao['nome']}**\n\n**{campeao['gasto_total']:.1f} L/dia**")

        st.divider()
        
        # 📈 GERANDO O GRÁFICO DE COLUNAS COM AS MÉDIAS (Sua nova solicitação!)
        st.subheader("📈 Placar Geral das Turmas")
        
        df_medias = df_geral.groupby("turma")["gasto_total"].mean().reset_index()
        todas_turmas = pd.DataFrame({"turma": TURMAS_OFICIAIS})
        df_medias = pd.merge(todas_turmas, df_medias, on="turma", how="left").fillna(0)
        
        fig, ax = plt.subplots(figsize=(7, 4))
        
        # Alterado de ax.plot para ax.bar para gerar colunas verticais
        barras = ax.bar(df_medias["turma"], df_medias["gasto_total"], color=['#3498db', '#3498db', '#3498db', '#2ecc71', '#2ecc71', '#2ecc71'], edgecolor='black', alpha=0.85)
        
        ax.set_ylabel("Litros Consumidos (Média)", fontsize=10)
        ax.set_title("Corrida Hídrica: Quem tem a menor coluna está ganhando!", fontsize=11, fontweight='bold')
        ax.grid(axis='y', linestyle='--', alpha=0.5) # Grid apenas nas linhas horizontais
        ax.set_ylim(0, max(df_medias["gasto_total"].max() + 30, 150))
        
        # Adiciona os valores numéricos em cima de cada coluna
        for barra in barras:
            altura = barra.get_height()
            ax.annotate(f"{altura:.1f} L",
                        xy=(barra.get_x() + barra.get_width() / 2, altura),
                        xytext=(0, 3),  # Deslocamento vertical do texto
                        textcoords="offset points",
                        ha='center', va='bottom', fontweight='bold')
            
        st.pyplot(fig)
        plt.close(fig)
        
        # 📋 TABELA COMPLETA DE DADOS
        st.subheader("📋 Tabela Geral de Auditoria (Dados Brutos do SQLite)")
        st.dataframe(df_geral[["nome", "turma", "gasto_total"]].sort_values(by="gasto_total"))

        # 🔒 PAINEL DO PROFESSOR PROTEGIDO POR SENHA
        st.divider()
        with st.expander("⚙️ Painel de Controle do Professor"):
            senha_professor = st.text_input("Digite a senha de administrador:", type="password")
            SENHA_CORRETA = "admin123"
            
            if senha_professor:
                if senha_professor == SENHA_CORRETA:
                    st.success("🔓 Acesso liberado, Professor!")
                    st.warning("⚠️ Zona de Perigo: As ações abaixo são irreversíveis.")
                    if st.button("🗑️ Resetar Gincana (Apagar Banco SQLite)"):
                        apagar_banco()
                        st.success("O banco de dados foi zerado com sucesso!")
                        st.rerun()
                else:
                    st.error("❌ Senha incorreta! Tente novamente.")

# --- ABA 3: SIMULADOR COLETIVO ---
with aba3:
    st.header("🌍 O Poder do Coletivo")
    tamanho_turma = st.slider("Tamanho da turma para simulação:", 10, 45, 30)
    
    gasto_antigo = 12 * VAZAO_CHUVEIRO 
    gasto_novo = 6 * VAZAO_CHUVEIRO 
    economia_mes = (gasto_antigo - gasto_novo) * tamanho_turma * 30

    st.metric("Economia Estimada por MÊS", f"{int(economia_mes):,} Litros")
    st.write(f"Isso equivale a **{int(economia_mes / 1000)} caixas d'água** de 1.000 litros cheias na Mirueira!")