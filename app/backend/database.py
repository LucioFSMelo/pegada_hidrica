import sqlite3
import pandas as pd
import os

DB_NAME = "gincana_hidrica.db"

def inicializar_banco():
    """Gera a estrutura de tabelas. Atualizado para arquitetura Multi-Estado."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Tabela de Professores 
    # [MODIFICAÇÃO PARA ESCALABILIDADE]: Adição das colunas 'uf' e 'municipio'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            disciplina TEXT NOT NULL,
            uf TEXT NOT NULL,
            municipio TEXT NOT NULL
        )
    """)
    
    # 2. Tabela de Vínculo: Professor x Escolas
    # [MODIFICAÇÃO PARA ESCALABILIDADE]: Adição de 'uf' e 'municipio' atrelados à escola
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS escolas_professor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            professor_email TEXT,
            nome_escola TEXT,
            uf TEXT NOT NULL,
            municipio TEXT NOT NULL,
            FOREIGN KEY (professor_email) REFERENCES professores(email)
        )
    """)
    
    # 3. Tabela de Alunos Oficiais da Escola
    # [MODIFICAÇÃO PARA ESCALABILIDADE]: Adição de 'uf' e 'municipio' para filtros precisos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo TEXT NOT NULL,
            turma TEXT NOT NULL,
            nome_escola TEXT NOT NULL,
            uf TEXT NOT NULL,
            municipio TEXT NOT NULL,
            UNIQUE(nome_completo, turma, nome_escola, uf, municipio)
        )
    """)
    
    # 4. Tabela de Consumo Hídrico
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consumo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            turma TEXT NOT NULL,
            nome_escola TEXT NOT NULL,
            gasto_banho REAL,
            gasto_escovacao REAL,
            gasto_total REAL
        )
    """)
    
    # 5. Tabela de Notas do Quiz
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_aluno TEXT NOT NULL,
            turma TEXT NOT NULL,
            nome_escola TEXT NOT NULL,
            pontuacao INTEGER
        )
    """)
    
    # 6. Painel de Controle Remoto (Status da Aula Ativa)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS controle_aula (
            id INTEGER PRIMARY KEY,
            turma_ativa TEXT DEFAULT 'FECHADO',
            escola_ativa TEXT DEFAULT '',
            modo_atual TEXT DEFAULT 'FECHADO'
        )
    """)
    
    cursor.execute("INSERT OR IGNORE INTO controle_aula (id, turma_ativa, escola_ativa, modo_atual) VALUES (1, 'FECHADO', '', 'FECHADO')")
    
    conn.commit()
    conn.close()

# =====================================================================
# 🔐 SISTEMA DE CADASTRO E LOGIN
# =====================================================================

# [MODIFICAÇÃO PARA ESCALABILIDADE]: Função agora recebe uf e municipio
def cadastrar_professor_completo(nome, email, senha, disciplina, uf, municipio, escolas):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        # Grava os dados do professor com localização
        cursor.execute("INSERT INTO professores (nome, email, senha, disciplina, uf, municipio) VALUES (?, ?, ?, ?, ?, ?)", 
                       (nome, email, senha, disciplina, uf, municipio.strip()))
        
        # Grava as escolas vinculando-as ao estado e município
        for escola in escolas:
            if escola.strip():
                cursor.execute("INSERT INTO escolas_professor (professor_email, nome_escola, uf, municipio) VALUES (?, ?, ?, ?)", 
                               (email, escola.strip(), uf, municipio.strip()))
        conn.commit()
        return True, "Cadastro realizado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Este e-mail já está cadastrado no sistema."
    finally:
        conn.close()

def login_professor_completo(email, senha):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT nome, email, disciplina FROM professores WHERE email = ? AND senha = ?", (email, senha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def buscar_escolas_do_professor(email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT nome_escola FROM escolas_professor WHERE professor_email = ?", (email,))
    escolas = [linha[0] for linha in cursor.fetchall()]
    conn.close()
    return escolas

# [MODIFICAÇÃO PARA ESCALABILIDADE]: Função de apoio para buscar a UF e Município de uma escola
def buscar_localizacao_da_escola(nome_escola):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT uf, municipio FROM escolas_professor WHERE nome_escola = ? LIMIT 1", (nome_escola,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return resultado[0], resultado[1]
    return "PE", "Desconhecido" # Fallback de segurança

# =====================================================================
# 🏫 REGRAS DE NEGÓCIO DA ESCOLA E ALUNOS
# =====================================================================

# [MODIFICAÇÃO PARA ESCALABILIDADE]: Importa os alunos já carimbando a UF e Município deles
def importar_alunos_via_dataframe(df, nome_escola):
    df.columns = [str(c).strip().lower() for c in df.columns]
    
    col_nome = None
    for col in df.columns:
        if 'nome' in col:
            col_nome = col
            break
            
    col_turma = None
    for col in df.columns:
        if 'turma' in col:
            col_turma = col
            break
    
    if not col_nome or not col_turma:
        return False, "O arquivo precisa de uma coluna com 'Nome'. E a Turma deve estar em uma coluna ou no nome da aba do Excel."
        
    uf_escola, municipio_escola = buscar_localizacao_da_escola(nome_escola)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    sucessos = 0
    
    for _, linha in df.iterrows():
        nome = str(linha[col_nome]).strip()
        turma = str(linha[col_turma]).strip()
        if nome and turma and nome.lower() != "nan" and turma.lower() != "nan":
            try:
                # [MODIFICAÇÃO] O aluno recebe a UF e o Municipio da escola
                cursor.execute(
                    "INSERT INTO alunos (nome_completo, turma, nome_escola, uf, municipio) VALUES (?, ?, ?, ?, ?)",
                    (nome, turma, nome_escola, uf_escola, municipio_escola)
                )
                sucessos += 1
            except sqlite3.IntegrityError:
                pass 
                
    conn.commit()
    conn.close()
    return True, f"Sucesso! {sucessos} novos alunos importados."

# =====================================================================
# 🌍 FILTROS EM CASCATA PARA A TELA DO ALUNO (NOVO MÓDULO)
# =====================================================================

# [MODIFICAÇÃO PARA ESCALABILIDADE]: Módulo exclusivo de listagem inteligente
def buscar_ufs_cadastradas():
    """Busca apenas os Estados (UF) que possuem alunos/escolas cadastradas."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT uf FROM alunos ORDER BY uf")
    ufs = [linha[0] for linha in cursor.fetchall()]
    conn.close()
    return ufs

def buscar_municipios_por_uf(uf):
    """Filtra os municípios baseados na UF escolhida."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT municipio FROM alunos WHERE uf = ? ORDER BY municipio", (uf,))
    muns = [linha[0] for linha in cursor.fetchall()]
    conn.close()
    return muns

def buscar_escolas_por_municipio(uf, municipio):
    """Filtra as escolas baseadas na UF e no Município escolhidos."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT nome_escola FROM alunos WHERE uf = ? AND municipio = ? ORDER BY nome_escola", (uf, municipio))
    escolas = [linha[0] for linha in cursor.fetchall()]
    conn.close()
    return escolas

def buscar_turmas_da_escola(nome_escola):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT turma FROM alunos WHERE nome_escola = ? ORDER BY turma", (nome_escola,))
    turmas = [linha[0] for linha in cursor.fetchall()]
    conn.close()
    return turmas

def verificar_aluno_matriculado(nome_completo, turma, nome_escola):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM alunos WHERE LOWER(nome_completo) = LOWER(?) AND LOWER(turma) = LOWER(?) AND LOWER(nome_escola) = LOWER(?)",
        (nome_completo.strip(), turma.strip(), nome_escola.strip())
    )
    existe = cursor.fetchone() is not None
    conn.close()
    return existe

# =====================================================================
# 🎛️ CONTROLE REMOTO DA AULA
# =====================================================================

def atualizar_controle_aula(turma, escola, modo):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE controle_aula SET turma_ativa = ?, escola_ativa = ?, modo_atual = ? WHERE id = 1", (turma, escola, modo))
    conn.commit()
    conn.close()

def verificar_turma_liberada():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT turma_ativa FROM controle_aula WHERE id = 1")
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado

def verificar_escola_liberada():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT escola_ativa FROM controle_aula WHERE id = 1")
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado

def verificar_modo_aula():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT modo_atual FROM controle_aula WHERE id = 1")
    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado

# =====================================================================
# 📥 GRAVAÇÃO DE DADOS E CONSULTAS DE APOIO
# =====================================================================

def salvar_no_banco(nome, turma, escola, gasto_banho, gasto_escovacao, gasto_total):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO consumo (nome, turma, nome_escola, gasto_banho, gasto_escovacao, gasto_total) VALUES (?, ?, ?, ?, ?, ?)",
        (nome, turma, escola, gasto_banho, gasto_escovacao, gasto_total)
    )
    conn.commit()
    conn.close()

def registrar_nota_quiz(escola, turma, nome_aluno, pontuacao):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO quiz_notas (nome_aluno, turma, nome_escola, pontuacao) VALUES (?, ?, ?, ?)",
        (nome_aluno, turma, escola, pontuacao)
    )
    conn.commit()
    conn.close()

def ler_dados_por_professor(nome_escola=None):
    """Busca os alunos no banco para renderização dos gráficos do professor."""
    conn = sqlite3.connect(DB_NAME)
    if nome_escola:
        df = pd.read_sql_query("SELECT * FROM alunos WHERE nome_escola = ?", conn, params=(nome_escola,))
    else:
        df = pd.read_sql_query("SELECT * FROM alunos", conn)
    conn.close()
    return df

# Novo --- O professor obtem os resultados do Quiz ---
def obter_resultados_quiz(escola, turma):
    """Busca todas as pontuações dos alunos de uma escola e turma específicas."""
    # Substitua pelo seu método real de conexão se não usar sqlite3 diretamente aqui
    conn = sqlite3.connect("sistema_escolar.db") 
    cursor = conn.cursor()
    
    try:
        # Busca o nome do aluno e a pontuação, ordenando do maior para o menor
        query = """
            SELECT nome_aluno, pontuacao, data_registro 
            FROM notas_quiz 
            WHERE escola = ? AND turma = ? 
            ORDER BY pontuacao DESC
        """
        df = pd.read_sql_query(query, conn, params=(escola, turma))
        conn.close()
        return df
    except Exception as e:
        conn.close()
        # Retorna um DataFrame vazio com as colunas caso a tabela ainda esteja vazia
        return pd.DataFrame(columns=["nome_aluno", "pontuacao", "data_registro"])

# Novo --- O professor pode Zerar o Quiz ---
def zerar_resultados_quiz(escola, turma):
    """Apaga os registros de pontuação do quiz para uma determinada turma."""
    conn = sqlite3.connect("sistema_escolar.db")
    cursor = conn.cursor()
    
    try:
        query = "DELETE FROM notas_quiz WHERE escola = ? AND turma = ?"
        cursor.execute(query, (escola, turma))
        conn.commit()
        conn.close()
        return True, "Pontuações zeradas com sucesso para esta turma!"
    except Exception as e:
        conn.close()
        return False, f"Erro ao zerar pontuações: {str(e)}"

if __name__ == "__main__":
    inicializar_banco()
    print("Banco de dados inicializado com sucesso!")