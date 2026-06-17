import sys
import os
import streamlit as st

# Garante o mapeamento de caminhos para o Python localizar a pasta raiz 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.backend.database import inicializar_banco

# Garante que as tabelas do banco de dados (e o cadeado do professor) existam ao abrir o app
inicializar_banco()

st.set_page_config(page_title="Detetives da Água - Home", page_icon="🏠", layout="centered")

# --- CONTEÚDO PRINCIPAL (HOME) ---
st.title("🏠 Objeto Digital de Aprendizagem: Detetives da Água")
st.markdown("---")

st.markdown("""
### 🍏 Guia de Orientação e Funcionalidades
Bem-vindo ao ecossistema **Detetives da Água**! Este projeto integra conceitos da BNCC através da computação prática e análise de dados reais coletados pelos próprios estudantes.

**Como funciona a dinâmica da aula?**
1. O professor acessa a aba **👨‍🏫 Professor** (no menu lateral), faz o login e **Destranca a Gincana** para a turma atual.
2. Os alunos acessam a aba **📊 Calculadora** (que só abrirá se estiver destrancada) e inserem seus dados de consumo.
3. Todos acompanham os resultados nas estações de **Ranking, Estatística, Funções e Financeiro**.
4. Ao final, os alunos testam seus conhecimentos na aba **🧠 Quiz**.
""")

# --- SEÇÃO DE DOWNLOAD (Com caminhos blindados) ---
st.divider()
st.subheader("📥 Baixar Material de Apoio da Aula")
st.markdown("Clique nos botões abaixo para baixar os slides e os guias em PDF utilizados nesta sequência didática:")

# Essa linha de mágica encontra a pasta "pegada_hidrica/" absoluta de forma automática
DIRETORIO_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Monta o caminho exato para encontrar os arquivos na raiz, não importa onde o app esteja rodando
caminho_pdf = os.path.join(DIRETORIO_RAIZ, "material_aula.pdf")
caminho_pptx = os.path.join(DIRETORIO_RAIZ, "material_aula.pptx")

col_pdf, col_pptx = st.columns(2)

with col_pdf:
    if os.path.exists(caminho_pdf):
        with open(caminho_pdf, "rb") as f:
            st.download_button(
                label="📄 Baixar Guia em PDF", 
                data=f, 
                file_name="Guia_Detetives.pdf", 
                mime="application/pdf"
            )
    else:
        st.caption("⚠️ Arquivo PDF não encontrado na raiz do projeto.")

with col_pptx:
    if os.path.exists(caminho_pptx):
        with open(caminho_pptx, "rb") as f:
            st.download_button(
                label="💻 Baixar Apresentação (PPTX)", 
                data=f, 
                file_name="Slides_Detetives.pptx", 
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
    else:
        st.caption("⚠️ Arquivo PPTX não encontrado na raiz do projeto.")

# --- RODAPÉ EMBUTIDO FIXO ---
st.markdown(
    """
    <style>
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: rgba(255, 255, 255, 0.9); color: #555555; text-align: center; padding: 8px 0; font-size: 13px; border-top: 1px solid #e0e0e0; z-index: 999; }
    @media (prefers-color-scheme: dark) { .footer { background-color: rgba(14, 17, 23, 0.9); color: #bbbbbb; border-top: 1px solid #262730; } }
    </style>
    <div class="footer"> © 2026 • Developed by Lucio Flavio • All Rights Reserved </div>
    """,
    unsafe_allow_html=True
)