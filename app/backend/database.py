import sqlite3
import pandas as pd

DB_NAME = "banco_pegada_hidrica.db"

def inicializar_banco():
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
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO consumo (nome, turma, gasto_banho, gasto_escovacao, gasto_total)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, turma, banho, escovacao, total))
    conn.commit()
    conn.close()

def ler_todos_dados():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM consumo", conn)
    conn.close()
    return df

def apagar_banco():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS consumo")
    conn.commit()
    conn.close()
    inicializar_banco()