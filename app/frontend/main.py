import sys
import os
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.backend.database import inicializar_banco

# Garante que as tabelas do banco de dados existam ao abrir o app
inicializar_banco()

st.set_page_config(page_title="Detetives da Água - Sistema", page_icon="🏠", layout="centered")

# --- BARRA LATERAL FIXA: BOTÃO DE DOAÇÃO ---
with st.sidebar:
    st.title("🌱 Apoie o Projeto")
    st.markdown("""
    Se este aplicativo ajudou suas turmas, considere fazer uma contribuição voluntária para nos ajudar a manter os servidores ativos!
    """)
    
    # Botão visual de doação estilizado profissionalmente com HTML e CSS
    st.markdown(
        """
        <a href="https://luciofsmelo.github.io/link-seu-pix" target="_blank" style="text-decoration: none;">
            <div style="background-color: #2ecc71; color: white; text-align: center; padding: 12px 20px; border-radius: 8px; font-weight: bold; font-size: 16px; box-shadow: 0px 4px 6px rgba(0,0,0,0.15); transition: 0.3s;">
                🪙 Contribuir / Doar via PIX
            </div>
        </a>
        """, 
        unsafe_allow_html=True
    )
    st.divider()
    st.caption("Desenvolvido para feiras de ciências e aulas de matemática/estatística.")

# --- CONTEÚDO PRINCIPAL (HOME) ---
st.title("🏠 Objeto Digital de Aprendizagem: Detetives da Água")
st.markdown("---")

st.markdown("""
### 🍏 Guia de Orientação ao Docente e Materiais de Apoio
Este ecossistema integra conceitos da BNCC através da computação prática e análise de dados reais coletados pelos próprios estudantes.
""")

# --- SEÇÃO DE DOWNLOAD DE MATERIAIS PARA O PROFESSOR ---
st.subheader("📥 Baixar Material de Apoio da Aula")
st.markdown("Clique nos botões abaixo para baixar os slides e os guias em PDF utilizados nesta sequência didática:")

col_pdf, col_pptx = st.columns(2)

with col_pdf:
    # O arquivo 'material_aula.pdf' deve ser colocado na pasta raiz do seu projeto (pegada_hidrica/)
    if os.path.exists("material_aula.pdf"):
        with open("material_aula.pdf", "rb") as f:
            st.download_button(
                label="📄 Baixar Guia em PDF",
                data=f,
                file_name="Guia_Detetives_da_Agua.pdf",
                mime="application/pdf"
            )
    else:
        st.caption("⚠️ Arquivo 'material_aula.pdf' não encontrado na pasta raiz.")

with col_pptx:
    # O arquivo 'material_aula.pptx' deve ser colocado na pasta raiz do seu projeto (pegada_hidrica/)
    if os.path.exists("material_aula.pptx"):
        with open("material_aula.pptx", "rb") as f:
            st.download_button(
                label="💻 Baixar Apresentação (PPTX)",
                data=f,
                file_name="Slides_Detetives_da_Agua.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
    else:
        st.caption("⚠️ Arquivo 'material_aula.pptx' não encontrado na pasta raiz.")

# --- SEÇÃO DO QUIZ INTERATIVO (CALIBRADO SOBRE CONSUMO E CONVERSÕES) ---
st.divider()
st.subheader("🧠 Desafio Interativo: O Quiz da Água")
st.markdown("Responda às questões abaixo para testar seu conhecimento sobre o consumo e unidades de medidas hídricas:")

# Banco de questões estruturado
perguntas = {
    "q1": {
        "titulo": "1. Se um estudante toma um banho de 10 minutos com o chuveiro aberto (vazão de 15L/min), qual será o consumo total?",
        "opcoes": ["15 litros", "50 litros", "150 litros", "1.500 litros"],
        "correta": "150 litros"
    },
    "q2": {
        "titulo": "2. As companhias de abastecimento cobram a tarifa de água baseada em qual unidade de medida?",
        "opcoes": ["Litros (L)", "Metros Cúbicos (m³)", "Mililitros (mL)", "Quilogramas (kg)"],
        "correta": "Metros Cúbicos (m³)"
    },
    "q3": {
        "titulo": "3. Um consumo registrado de 15.000 litros de água equivale a quantos metros cúbicos (m³)?",
        "opcoes": ["1.5 m³", "15 m³", "150 m³", "0.15 m³"],
        "correta": "15 m³"
    }
}

# Renderização das perguntas no Streamlit
r1 = st.radio(perguntas["q1"]["titulo"], perguntas["q1"]["opcoes"])
st.write("")
r2 = st.radio(perguntas["q2"]["titulo"], perguntas["q2"]["opcoes"])
st.write("")
r3 = st.radio(perguntas["q3"]["titulo"], perguntas["q3"]["opcoes"])

# Botão de correção do Quiz
if st.button("🏁 Corrigir Meu Quiz"):
    acertos = 0
    if r1 == perguntas["q1"]["correta"]: acertos += 1
    if r2 == perguntas["q2"]["correta"]: acertos += 1
    if r3 == perguntas["q3"]["correta"]: acertos += 1
    
    if acertos == 3:
        st.success(f"🥇 Espetacular! Você acertou todas as {acertos} questões. Um verdadeiro mestre na economia de água!")
    elif acertos > 0:
        st.warning(f"✍️ Bom esforço! Você acertou {acertos} de 3 questões. Revise os cálculos e tente gabaritar!")
    else:
        st.error("❌ Nenhuma resposta correta. Releia o material didático e tente de novo!")

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