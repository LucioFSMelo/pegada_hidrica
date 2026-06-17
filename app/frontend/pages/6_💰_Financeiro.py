import sys
import os
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

st.set_page_config(page_title="Estação Financeira", page_icon="💰", layout="centered")

st.header("💰 Estação 3: Unidades de Medida e Conta de Água")
st.markdown("""
As companhias de saneamento básico não cobram a água em litros, mas sim em **Metros Cúbicos ($m^3$)**.
Vamos entender essa conversão e calcular o impacto financeiro!
""")

# Caixa didática explicando a conversão de volume
st.warning("""
📐 **Regra Fundamental de Conversão:**
$$1 \text{ m}^3 = 1.000 \text{ litros de água}$$
Portanto, para transformar litros em metros cúbicos, dividimos o valor por 1.000!
""")

st.divider()

st.subheader("💵 Simulador de Tarifa Residencial")
st.markdown("Insira o consumo mensal estimado de uma família (em Litros) para ver a conversão e o custo financeiro aproximado.")

consumo_litros_mes = st.number_input("Digite o consumo mensal da família em LITROS:", min_value=1000, value=15000, step=1000)

# Realiza a conversão de unidades de volume
consumo_m3 = consumo_litros_mes / 1000

st.info(f"🔄 **Conversão:** {consumo_litros_mes:,} Litros equivalem a **{consumo_m3:.2f} $m^3$** de água.")

# --- SIMULAÇÃO SIMPLIFICADA DE TARIFAS ---
# Baseado em modelos de tarifas sociais/comuns brasileiras por faixas de consumo
TARIFA_MINIMA = 45.00 # Até 10m³ paga-se uma taxa fixa
PRECO_POR_M3_EXCEDENTE = 7.50 # Valor por m³ acima de 10m³

if consumo_m3 <= 10:
    valor_conta = TARIFA_MINIMA
    detalhe_calculo = "Sua família ficou na faixa de consumo mínimo residencial (Até 10 m³)."
else:
    m3_excedentes = consumo_m3 - 10
    valor_conta = TARIFA_MINIMA + (m3_excedentes * PRECO_POR_M3_EXCEDENTE)
    detalhe_calculo = f"Tarifa Mínima (R$ 45,00) + {m3_excedentes:.1f} m³ excedentes a R$ {PRECO_POR_M3_EXCEDENTE:.2f} cada."

st.divider()
st.subheader("🧾 Estimativa da Conta de Água")
st.metric("Valor Estimado da Tarifa de Água", f"R$ {valor_conta:.2f}")
st.caption(f"**Nota de cálculo:** {detalhe_calculo}")

st.markdown("""
---
### 🔍 Como ler o Hidrômetro (O medidor da sua casa)?
Quando você olha para o relógio de água da sua calçada:
* Os **números PRETOS** registram o volume em **Metros Cúbicos ($m^3$)** — são esses números que a companhia lê para gerar a conta.
* Os **números VERMELHOS** ou ponteiros menores registram os **Litros** gastados em tempo real.
""")