import sys
import os
import streamlit as st

# Garante o mapeamento de caminhos para o Python localizar a pasta raiz 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.backend.database import inicializar_banco

# Garante que as tabelas do banco de dados (e o cadeado do professor) existam ao abrir o app
inicializar_banco()

# =====================================================================
# 🏡 FUNÇÃO PÁGINA HOME (Todo o conteúdo visual mesclado aqui)
# =====================================================================
def renderizar_home():
    st.title("🏠 Plataforma de Aprendizagem: Detetives da Água", text_alignment="center")
    st.markdown("---")
    st.subheader("**🚱 Missão: Pegada Hídrica**", text_alignment="center")
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

    # --- SEÇÃO DE DOWNLOAD (Apontando para a nova pasta assets) ---
    st.divider()
    st.subheader("📥 Baixar Material de Apoio da Aula")
    st.markdown("Clique nos botões abaixo para baixar a apresentação em slides ou em PDF utilizados nesta sequência didática:")

    # Encontra dinamicamente a pasta 'assets' dentro de 'frontend'
    DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
    PASTA_ASSETS = os.path.join(DIRETORIO_ATUAL, "assets")

    # Monta o caminho exato usando o nome que você definiu
    caminho_pdf = os.path.join(PASTA_ASSETS, "MISSÃO_DETETIVES_DA_ÁGUA.pdf")
    caminho_pptx = os.path.join(PASTA_ASSETS, "MISSÃO_DETETIVES_DA_ÁGUA.pptx")

    col_pdf, col_pptx = st.columns(2)

    with col_pdf:
        if os.path.exists(caminho_pdf):
            with open(caminho_pdf, "rb") as f:
                st.download_button(
                    label="📄 Baixar Apresentação em PDF", 
                    data=f, 
                    file_name="Missao_Detetives_da_Agua.pdf", 
                    mime="application/pdf"
                )
        else:
            st.caption("⚠️ Arquivo PDF não encontrado na pasta assets.")

    with col_pptx:
        if os.path.exists(caminho_pptx):
            with open(caminho_pptx, "rb") as f:
                st.download_button(
                    label="💻 Baixar Apresentação (PPTX)", 
                    data=f, 
                    file_name="Missao_Detetives_da_Agua.pptx", 
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
        else:
            st.caption("⚠️ Arquivo PPTX não encontrado na pasta assets.")

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

# =====================================================================
# 🥾 BOOTSTRAP DE NAVEGAÇÃO PROFISSIONAL (Via Função Callback)
# =====================================================================
# Mapeia as páginas e passa a função renderizar_home para evitar o erro de recursão (loop infinito)
pagina_home = st.Page(renderizar_home, title="Home", icon="🏠", default=True)
pagina_prof = st.Page("pages/1_👨‍🏫_Professor.py", title="Professor", icon="👨‍🏫")
pagina_quiz = st.Page("pages/2_🧠_Quiz.py", title="Quiz", icon="🧠")
pagina_apoi = st.Page("pages/3_🌱_Apoie.py", title="Apoie o projeto", icon="🌱")

# O gerenciador de rotas agrupa as páginas no menu lateral nativamente
pg = st.navigation([pagina_home, pagina_prof, pagina_quiz, pagina_apoi])

# Executa o roteador (Isso configura o título, ícone e renderiza a página selecionada com segurança)
pg.run()
# =====================================================================