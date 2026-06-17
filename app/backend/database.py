import sqlite3
import datetime
import hashlib
import pandas as pd

DB_NAME = "banco_pegada_hidrica.db"

def gerar_hash_senha(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def inicializar_banco():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Tabela de consumo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consumo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT, turma TEXT, gasto_banho REAL, gasto_escovacao REAL, gasto_total REAL, data_registro TEXT
        )
    """)
    # Tabela de professores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professores (usuario TEXT PRIMARY KEY, senha_criptografada TEXT)
    """)
    # Tabela de Turmas vinculadas ao professor
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turmas (id INTEGER PRIMARY KEY AUTOINCREMENT, nome_turma TEXT UNIQUE, professor_usuario TEXT)
    """)
    # Tabela para travar/destravar o aplicativo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sistema (chave TEXT PRIMARY KEY, valor TEXT)
    """)
    cursor.execute("INSERT OR IGNORE INTO sistema (chave, valor) VALUES ('turma_liberada', 'FECHADO')")
    
    conn.commit()
    conn.close()

# --- FUNÇÕES DE CONTROLE DE ACESSO (O CADEADO) ---
def definir_turma_liberada(turma):
    """Muda o status do sistema para liberar o app para uma turma específica (ou FECHADO)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE sistema SET valor = ? WHERE chave = 'turma_liberada'", (turma,))
    conn.commit()
    conn.close()

def verificar_turma_liberada():
    """Checa se o professor liberou o app. Se não, retorna 'FECHADO'."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT valor FROM sistema WHERE chave = 'turma_liberada'")
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else "FECHADO"

# --- FUNÇÕES DO PROFESSOR ---
def login_ou_cadastro_professor(usuario, senha_digitada):
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
        return "SENHA_INCORRETA"
    else:
        if usuario_limpo == "" or senha_digitada.strip() == "": return "CAMPOS_VAZIOS"
        cursor.execute("INSERT INTO professores (usuario, senha_criptografada) VALUES (?, ?)", (usuario_limpo, senha_hash))
        conn.commit()
        conn.close()
        return "NOVO_CADASTRO"

def adicionar_turma(usuario, nome_turma):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    turma_formatada = nome_turma.strip().upper()
    try:
        cursor.execute("INSERT INTO turmas (nome_turma, professor_usuario) VALUES (?, ?)", (turma_formatada, usuario.strip().lower()))
        conn.commit()
        sucesso = True
    except sqlite3.IntegrityError:
        sucesso = False # Turma já existe
    conn.close()
    return sucesso

def buscar_turmas_do_professor(usuario):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT nome_turma FROM turmas WHERE professor_usuario = ?", (usuario.strip().lower(),))
    turmas = [linha[0] for linha in cursor.fetchall()]
    conn.close()
    return sorted(turmas)

def buscar_turmas_ativas():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT nome_turma FROM turmas")
    turmas = [linha[0] for linha in cursor.fetchall()]
    conn.close()
    return sorted(turmas)

# --- FUNÇÕES DE DADOS (MANTIDAS) ---
def salvar_no_banco(nome, turma, gasto_banho, gasto_escovacao, gasto_total):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO consumo (nome, turma, gasto_banho, gasto_escovacao, gasto_total, data_registro) VALUES (?, ?, ?, ?, ?, ?)", (nome, turma, gasto_banho, gasto_escovacao, gasto_total, data_atual))
    conn.commit()
    conn.close()

def ler_todos_dados():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM consumo", conn)
    conn.close()
    return df

def apagar_dados_por_turma(turma):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM consumo WHERE turma = ?", (turma,))
    conn.commit()
    conn.close()