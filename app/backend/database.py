import sqlite3
import datetime
import pandas as pd

DB_NAME = "banco_pegada_hidrica.db"

def inicializar_banco():
    """Cria o banco de dados e as tabelas necessárias se não existirem."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Tabela de consumo dos alunos (adicionada a coluna data_registro)
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
    
    # Tabela de logins dos professores vinculados às suas respectivas turmas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professores (
            usuario TEXT PRIMARY KEY,
            senha TEXT NOT NULL,
            turma_gerenciada TEXT NOT NULL
        )
    """)
    
    # Cria professores padrão para testes caso a tabela esteja vazia
    cursor.execute("SELECT COUNT(*) FROM professores")
    if cursor.fetchone()[0] == 0:
        professores_iniciais = [
            ("lucio8a", "senha123", "8º A"),
            ("professor8b", "senha123", "8º B"),
            ("professor8c", "senha123", "8º C"),
            ("professor9a", "senha123", "9º A"),
            ("professor9b", "senha123", "9º B"),
            ("professor9c", "senha123", "9º C"),
        ]
        cursor.executemany("INSERT INTO professores (usuario, senha, turma_gerenciada) VALUES (?, ?, ?)", professores_iniciais)
    
    conn.commit()
    conn.close()

def salvar_no_banco(nome, turma, gasto_banho, gasto_escovacao, gasto_total):
    """Salva os dados do aluno incluindo o carimbo de data/hora atual."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Captura a data e hora exata do envio
    data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO consumo (nome, turma, gasto_banho, gasto_escovacao, gasto_total, data_registro)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, turma, gasto_banho, gasto_escovacao, gasto_total, data_atual))
    
    conn.commit()
    conn.close()

def ler_todos_dados():
    """Retorna um DataFrame com todos os registros de consumo do banco."""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM consumo", conn)
    conn.close()
    return df

def verificar_login_professor(usuario, senha):
    """Verifica se as credenciais do professor existem e retorna a turma dele."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT turma_gerenciada FROM professores WHERE usuario = ? AND senha = ?", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def apagar_dados_por_turma(turma):
    """Permite que um professor limpe manualmente APENAS os dados da sua turma."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM consumo WHERE turma = ?", (turma,))
    conn.commit()
    conn.close()

def rotina_autolimpeza_15_dias(turma):
    """Executa a limpeza automática de dados com mais de 15 dias para evitar sobrecarga."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Calcula a data exata de 15 dias atrás
    data_limite = (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%Y-%m-%d %H:%M:%S")
    
    # Deleta apenas os registros antigos daquela turma específica
    cursor.execute("DELETE FROM consumo WHERE turma = ? AND data_registro < ?", (turma, data_limite))
    
    conn.commit()
    conn.close()