import streamlit as st

st.set_page_config(page_title="Apoie o Projeto", page_icon="🌱", layout="centered")

st.title("🌱 Apoie o Projeto Detetives da Água")
st.markdown("""
Se este aplicativo ajudou suas turmas a compreenderem melhor o consumo hídrico e a matemática, considere fazer uma contribuição voluntária para nos ajudar a manter os servidores do banco de dados ativos e gratuitos para escolas públicas!
""")

# IMPORTANTE: Substitua os links abaixo ('https://...') pelos links reais gerados no seu banco
link_10_reais = "https://nubank.com.br/cobrar/1fkkil/6a31c705-3575-4cd8-a16d-78a1340fcfa0"
link_15_reais = "https://nubank.com.br/cobrar/1fkkil/6a31c7f8-9e1a-416c-be9a-0661b1d66f66"
link_20_reais = "https://nubank.com.br/cobrar/1fkkil/6a31c832-90b7-4df2-b7f0-5ec4ca9187e1"

# Botões de doação estilizados
st.markdown(f"""
    <a href="{link_10_reais}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #3498db; color: white; text-align: center; padding: 15px; margin-bottom: 15px; border-radius: 8px; font-weight: bold; font-size: 16px; box-shadow: 0px 4px 6px rgba(0,0,0,0.1);">
            🪙 Contribuir com R$ 10,00
        </div>
    </a>
    
    <a href="{link_15_reais}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #2ecc71; color: white; text-align: center; padding: 15px; margin-bottom: 15px; border-radius: 8px; font-weight: bold; font-size: 16px; box-shadow: 0px 4px 6px rgba(0,0,0,0.1);">
            💚 Contribuir com R$ 15,00 (Recomendado)
        </div>
    </a>
    
    <a href="{link_20_reais}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #9b59b6; color: white; text-align: center; padding: 15px; margin-bottom: 15px; border-radius: 8px; font-weight: bold; font-size: 16px; box-shadow: 0px 4px 6px rgba(0,0,0,0.1);">
            💎 Contribuir com R$ 20,00
        </div>
    </a>
""", unsafe_allow_html=True)

st.divider()
st.info("💡 Todo o valor arrecadado é revertido para os custos de hospedagem na nuvem e melhorias na plataforma educacional.")