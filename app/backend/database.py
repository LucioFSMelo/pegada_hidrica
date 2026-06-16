import sqlite3
import datetime
import hashlib
import pandas as pd

DB_NAME = "banco_pegada_hidrica.db"

def gerar_hash_senha(senha_pura):
    """Transforma uma senha de texto limpo em um código seguro (Hash SHA-256)."""
    return hashlib.sha256(senha_pura.encode('utf-8')).hexdigest()

def inicializar_banco():
    """Cria as tabelas necessárias sem nenhuma turma padrão."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Tabela de consumo dos alunos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consumo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turma TEXT NOT NULL,
            gasto_banho REAL,
            gasto_escovacao REAL,
            gasto_total REAL,
            data_registro TEXT NOT NULL 
        )
    """)
    
    # Tabela de professores (gerenciadores de turmas)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professores (
            usuario TEXT PRIMARY KEY,
            senha_criptografada TEXT NOT NULL,
            turma_gerenciada TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def login_ou_cadastro_professor(usuario, senha_digitada, turma_digitada):
    """
    Verifica o login do professor. Se o usuário não existir, cria o cadastro
    automaticamente vinculado à turma informada.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    senha_hash = gerar_hash_senha(senha_digitada)
    usuario_limpo = usuario.strip().lower()
    turma_formatada = turma_digitada.strip().upper() # Padroniza para maiúsculas (ex: 6º A)
    
    # Verifica se o usuário já existe
    cursor.execute("SELECT senha_criptografada, turma_gerenciada FROM professores WHERE usuario = ?", (usuario_limpo,))
    professor = cursor.fetchone()
    
    if professor:
        # Se existe, verifica se a senha bate
        if professor[0] == senha_hash:
            conn.close()
            return professor[1] # Retorna a turma gerenciada gravada no banco
        else:
            conn.close()
            return "SENHA_INCORRETA"
    else:
        # Se o usuário NÃO existe, cria um novo professor e uma nova turma na hora!
        if usuario_limpo == "" or senha_digitada.strip() == "" or turma_formatada == "":
            conn.close()
            return "CAMPOS_VAZIOS"
            
        cursor.execute("""
            INSERT INTO professores (usuario, senha_criptografada, turma_gerenciada)
            VALUES (?, ?, ?)
        """, (usuario_limpo, senha_hash, turma_formatada))
        conn.commit()
        conn.close()
        return turma_formatada

def buscar_turmas_ativas():
    """Retorna uma lista de todas as turmas que possuem professores ou alunos cadastrados."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Coleta turmas da tabela de professores e alunos para cruzar os dados dinamicamente
    cursor.execute("SELECT turma_gerenciada FROM professores UNION SELECT turma FROM consumo")
    turmas = [linha[0] for linha in cursor.fetchall() if linha[0]]
    
    conn.close()
    return sorted(turmas) # Retorna em ordem alfabética/numérica natural

# --- Funções mantidas após refatoração ---

def salvar_no_banco(nome, turma, gasto_banho, gasto_escovacao, gasto_total):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO consumo (nome, turma, gasto_banho, gasto_escovacao, gasto_total, data_registro)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome.strip(), turma.strip().upper(), gasto_banho, gasto_escovacao, gasto_total, data_atual))
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

def rotina_autolimpeza_15_dias(turma):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    data_limite = (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("DELETE FROM consumo WHERE turma = ? AND data_registro < ?", (turma, data_limite))
    conn.commit()
    conn.close()