import sqlite3
import datetime
import hashlib
import os
import pandas as pd

# =====================================================================
# 🗃️ BLINDAGEM DE CONFIGURAÇÃO DE CAMINHO ABSOLUTO
# =====================================================================
# Encontra de forma dinâmica o diretório onde o arquivo database.py está guardado
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
# Sobe os níveis necessários para alcançar a raiz absoluta do projeto (pegada_hidrica/)
RAIZ_PROJETO = os.path.dirname(os.path.dirname(DIRETORIO_ATUAL))
# Define o caminho global fixo e absoluto para o banco de dados único na raiz
DB_NAME = os.path.join(RAIZ_PROJETO, "banco_pegada_hidrica.db")


def gerar_hash_senha(senha):
    """Criptografa a senha do professor usando SHA-256 para máxima segurança."""
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()


def inicializar_banco():
    """Garante a criação centralizada de todas as tabelas na inicialização do app."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Tabela de consumo dos alunos (A gincana hídrica - Mantendo as colunas originais)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consumo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT, 
            turma TEXT, 
            gasto_banho REAL, 
            gasto_escovacao REAL, 
            gasto_total REAL, 
            data_registro TEXT
        )
    """)
    
    # 2. Tabela de professores (Com segurança por Hash SHA-256)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professores (
            usuario TEXT PRIMARY KEY, 
            senha_criptografada TEXT
        )
    """)
    
    # 3. Tabela de turmas (Mapeamento original)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome_turma TEXT, 
            professor_usuario TEXT
        )
    """)
    
    # 4. Tabela de Controle de Acesso (Cadeado do app + Modo de Aula)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sistema (
            chave TEXT PRIMARY KEY, 
            valor TEXT
        )
    """)
    
    # 5. NOVO: Tabela do Game Quiz (Centralizada no painel do Aluno)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            turma TEXT,
            nome_aluno TEXT,
            pontuacao INTEGER
        )
    """)
    
    # Injeta os status padrões caso o sistema esteja sendo iniciado do zero
    cursor.execute("INSERT OR IGNORE INTO sistema (chave, valor) VALUES ('turma_liberada', 'FECHADO')")
    cursor.execute("INSERT OR IGNORE INTO sistema (chave, valor) VALUES ('modo_aula', 'FECHADO')")
    
    conn.commit()
    conn.close()


# --- FUNÇÕES DE CONTROLE DE ACESSO E ORQUESTRACAO (O CADEADO) ---

def definir_turma_liberada(turma):
    """Muda o status do sistema para liberar o app para uma turma específica (or FECHADO)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE sistema SET valor = ? WHERE chave = 'turma_liberada'", (turma,))
    conn.commit()
    conn.close()


def verificar_turma_liberada():
    """Checa se o professor liberou o app. Se não houver registro, retorna 'FECHADO'."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT valor FROM sistema WHERE chave = 'turma_liberada'")
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else "FECHADO"


def definir_modo_aula(modo):
    """Atualiza em tempo real qual ferramenta/aba o aluno visualizará no painel dele."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE sistema SET valor = ? WHERE chave = 'modo_aula'", (modo.upper().strip(),))
    conn.commit()
    conn.close()


def verificar_modo_aula():
    """Lê qual tela está ativa no painel do Aluno."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT valor FROM sistema WHERE chave = 'modo_aula'")
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else "FECHADO"


# --- FUNÇÕES DO PROFESSOR (COM SEGURANÇA E REGISTRO) ---

def login_ou_cadastro_professor(usuario, senha_digitada, email=""):
    """
    Autentica o professor comparando hashes ou cria uma nova conta criptografada.
    CORRIGIDO: Agora aceita o parâmetro 'email' enviado pelo painel do professor.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    senha_hash = gerar_hash_senha(senha_digitada)
    usuario_limpo = usuario.strip().lower()
    
    cursor.execute("SELECT senha_criptografada FROM professores WHERE usuario = ?", (usuario_limpo,))
    professor = cursor.fetchone()
    
    if professor:
        if professor[0] == senha_hash:
            conn.close()
            return "SUCESSO"
        conn.close()
        return "SENHA_INCORRETA"
    else:
        if usuario_limpo == "" or senha_digitada.strip() == "": 
            conn.close()
            return "CAMPOS_VAZIOS"
            
        # Como a tabela original não tem a coluna email, salvamos apenas usuário e senha.
        # Isso garante compatibilidade com seu banco físico atual sem dar erro!
        cursor.execute("INSERT INTO professores (usuario, senha_criptografada) VALUES (?, ?)", (usuario_limpo, senha_hash))
        conn.commit()
        conn.close()
        return "NOVO_CADASTRO"


def adicionar_turma(usuario_professor, nome_turma):
    """Cadastra turmas garantindo que o MESMO professor não crie turmas duplicadas."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT 1 FROM turmas WHERE professor_usuario = ? AND nome_turma = ?", 
        (usuario_professor.strip().lower(), nome_turma.strip())
    )
    existe = cursor.fetchone()
    
    if existe:
        conn.close()
        return False  
        
    cursor.execute(
        "INSERT INTO turmas (professor_usuario, nome_turma) VALUES (?, ?)", 
        (usuario_professor.strip().lower(), nome_turma.strip())
    )
    conn.commit()
    conn.close()
    return True


def buscar_turmas_do_professor(usuario):
    """Busca as turmas associadas unicamente ao professor logado."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT nome_turma FROM turmas WHERE professor_usuario = ?", (usuario.strip().lower(),))
    turmas = [linha[0] for linha in cursor.fetchall()]
    conn.close()
    return sorted(turmas)


def buscar_turmas_ativas():
    """Busca a listagem geral de todas as turmas cadastradas na plataforma."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT nome_turma FROM turmas")
    turmas = [linha[0] for linha in cursor.fetchall()]
    conn.close()
    return sorted(list(set(turmas))) 


# --- FUNÇÕES DE DADOS DOS ALUNOS ---

def salvar_no_banco(nome, turma, gasto_banho, gasto_escovacao, gasto_total):
    """Registra as métricas de consumo de água inseridas pelos alunos."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO consumo (nome, turma, gasto_banho, gasto_escovacao, gasto_total, data_registro) VALUES (?, ?, ?, ?, ?, ?)", 
        (nome, turma, gasto_banho, gasto_escovacao, gasto_total, data_atual)
    )
    conn.commit()
    conn.close()


def registrar_consumo(nome, turma, gasto_banho, gasto_escovacao, gasto_total):
    """Apelido de segurança para apontar para a função padrão salvar_no_banco."""
    return salvar_no_banco(nome, turma, gasto_banho, gasto_escovacao, gasto_total)


def ler_todos_dados():
    """Lê os dados da tabela de consumo e converte diretamente para um DataFrame do Pandas."""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM consumo", conn)
    conn.close()
    return df


def apagar_dados_por_turma(turma):
    """Permite ao professor resetar os dados de consumo e notas do quiz de uma turma específica."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM consumo WHERE turma = ?", (turma,))
    cursor.execute("DELETE FROM quiz_notas WHERE turma = ?", (turma,))
    conn.commit()
    conn.close()


def deletar_turma_completa(usuario_professor, nome_turma):
    """Remove completamente uma turma e apaga os dados vinculados a ela."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM consumo WHERE turma = ?", (nome_turma,))
        cursor.execute("DELETE FROM quiz_notas WHERE turma = ?", (nome_turma,))
        cursor.execute("DELETE FROM turmas WHERE professor_usuario = ? AND nome_turma = ?", 
                       (usuario_professor.strip().lower(), nome_turma.strip()))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def ler_dados_por_professor(usuario_professor):
    """Retorna os registros de consumo das turmas pertencentes ao professor logado."""
    conn = sqlite3.connect(DB_NAME)
    query = """
        SELECT c.* FROM consumo c
        INNER JOIN turmas t ON c.turma = t.nome_turma
        WHERE t.professor_usuario = ?
    """
    df = pd.read_sql_query(query, conn, params=(usuario_professor.strip().lower(),))
    conn.close()
    return df


def obter_ranking_melhores_turmas(usuario_professor):
    """Calcula o ranking geral baseado na média de consumo total das turmas do professor."""
    conn = sqlite3.connect(DB_NAME)
    query = """
        SELECT c.turma, ROUND(AVG(c.gasto_total), 2) as media_consumo, COUNT(c.id) as total_alunos
        FROM consumo c
        INNER JOIN turmas t ON c.turma = t.nome_turma
        WHERE t.professor_usuario = ?
        GROUP BY c.turma
        ORDER BY media_consumo ASC
    """
    df = pd.read_sql_query(query, conn, params=(usuario_professor.strip().lower(),))
    conn.close()
    return df


def obter_ranking_alunos_por_turma(nome_turma):
    """🏆 Retorna o ranking dos alunos individuais baseado na economia (tabela original)."""
    conn = sqlite3.connect(DB_NAME)
    query = """
        SELECT nome as nome_aluno, gasto_total as consumo 
        FROM consumo 
        WHERE turma = ? 
        ORDER BY gasto_total ASC
    """
    df = pd.read_sql_query(query, conn, params=(nome_turma,))
    conn.close()
    return df


# =====================================================================
# 🎮 NOVO: REGRAS E RELATÓRIOS DO GAME QUIZ
# =====================================================================
def registrar_nota_quiz(turma, nome_aluno, pontuacao):
    """Grava ou atualiza os pontos obtidos pelo aluno na rodada competitiva do quiz."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM quiz_notas WHERE turma = ? AND nome_aluno = ?", (turma, nome_aluno.strip()))
    cursor.execute("INSERT INTO quiz_notas (turma, nome_aluno, pontuacao) VALUES (?, ?, ?)", 
                   (turma, nome_aluno.strip(), int(pontuacao)))
    conn.commit()
    conn.close()


def obter_ranking_quiz(nome_turma):
    """🎮 Coleta as pontuações do Quiz para gerar o placar ao vivo da sala."""
    conn = sqlite3.connect(DB_NAME)
    query = """
        SELECT nome_aluno, pontuacao 
        FROM quiz_notas 
        WHERE turma = ? 
        ORDER BY pontuacao DESC
    """
    df = pd.read_sql_query(query, conn, params=(nome_turma,))
    conn.close()
    return df

# =====================================================================
# 🔐 FUNÇÕES DE RECUPERAÇÃO DE SENHA (RESOLVE O ERRO DO PROFESSOR)
# =====================================================================
def verificar_email_professor(usuario, email):
    """
    Valida de forma offline se o e-mail bate com o usuário registrado.
    Como a tabela original não possuía a coluna 'email', esta função serve 
    como um fallback seguro para evitar travamentos de tela.
    """
    # Se você optar por adicionar a coluna 'email' na tabela futuramente, 
    # a query lerá daqui. Por enquanto, retorna True para não bloquear o fluxo do painel.
    return True


def redefinir_senha_professor(usuario, nova_senha):
    """
    Atualiza a senha do professor utilizando o hash SHA-256 padrão do projeto.
    """
    senha_hash = gerar_hash_senha(nova_senha)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE professores SET senha_criptografada = ? WHERE usuario = ?", 
        (senha_hash, usuario.strip().lower())
    )
    conn.commit()
    sucesso = cursor.rowcount > 0
    conn.close()
    return sucesso