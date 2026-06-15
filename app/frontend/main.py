import sys
import os
import streamlit as st

# Solução de caminho de módulo (sys.path) para garantir o deploy sem erros
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.backend.database import inicializar_banco

# Inicializa o banco SQLite logo na abertura do app
inicializar_banco()

# Configuração da Página Principal
st.set_page_config(
    page_title="Detetives da Água - Guia Pedagógico",
    page_icon="🏠",
    layout="centered"
)

st.title("🏠 Objeto Digital de Aprendizagem: Detetives da Água")
st.markdown("---")

st.markdown("""
### 🍏 Guia de Orientação ao Docente
Este aplicativo foi desenvolvido para ser um **recurso didático interdisciplinar**, integrando conceitos de **Matemática, Ciências e Cidadania** através do estudo da pegada hídrica individual e coletiva.

#### 🎯 Competências e Habilidades Trabalhadas (BNCC)
* **Ciências (EF09CI13):** Propor iniciativas individuais e coletivas para a solução de problemas ambientais, como o uso consciente da água.
* **Matemática (EF09MA22):** Escolher o gráfico mais adequado para apresentar um conjunto de dados estatísticos e interpretar tabelas de frequência.
* **Matemática (EF09MA06):** Compreender as funções como relações de dependência entre duas variáveis, analisando suas representações algébricas e gráficas.

---

### 🗺️ Como navegar pelas Estações de Aprendizagem?
Utilize o **menu lateral esquerdo** para guiar os estudantes pelas atividades:

1. **📊 Calculadora:** Onde cada estudante insere seus dados de consumo diário (coleta de dados).
2. **🏆 Ranking:** Exibição do pódio e auditoria dos dados do banco SQLite.
3. **📈 Estatística:** Análise de médias aritméticas e tabelas de frequência.
4. **🧮 Funções:** Estudo algébrico e modelagem matemática do consumo.
5. **💰 Financeiro:** Conversão de $m^3$ e simulação do impacto financeiro na conta de água.
""")

st.info("💡 **Dica Pedagógica:** Recomenda-se projetar esta página inicial no início da aula para contextualizar a atividade com os estudantes antes de liberar o link de acesso aos celulares.")

# --- Criador do Aplicativo ---
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.9); /* Fundo branco semi-transparente */
        color: #555555; /* Cor do texto cinza escuro */
        text-align: center;
        padding: 8px 0;
        font-size: 13px;
        font-weight: 500;
        letter-spacing: 0.5px;
        border-top: 1px solid #e0e0e0;
        z-index: 999;
    }
    /* Adaptação automática para o modo escuro do Streamlit */
    @media (prefers-color-scheme: dark) {
        .footer {
            background-color: rgba(14, 17, 23, 0.9);
            color: #bbbbbb;
            border-top: 1px solid #262730;
        }
    }
    </style>
    <div class="footer">
        © 2026 • Developed by Lucio Flavio • All Rights Reserved
    </div>
    """,
    unsafe_allow_html=True
)