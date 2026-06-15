import sys
import os
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from app.backend.calculator import VAZAO_CHUVEIRO, VAZAO_TORNEIRA_PIA

st.set_page_config(page_title="Estação Álgebra", page_icon="🧮", layout="centered")

st.header("🧮 Estação 2: Modelagem Matemática e Funções")
st.markdown("""
O consumo de água pode ser representado matematicamente por uma **Função Linear de duas variáveis**.
A quantidade de água consumida depende diretamente do tempo em que as torneiras e chuveiros ficam ligados!
""")

# Exibição da equação usando LaTeX (Formatação matemática científica elegante)
st.latex(r"f(x, y) = a \cdot x + b \cdot y")
st.markdown(f"""
Onde:
* **$f(x, y)$** = Consumo total de água em litros.
* **$a$** = Vazão do chuveiro (**{VAZAO_CHUVEIRO} Litros/minuto**).
* **$x$** = Tempo de banho (variável independente 1).
* **$b$** = Vazão da torneira (**{VAZAO_TORNEIRA_PIA} Litros/minuto**).
* **$y$** = Tempo de torneira aberta (variável independente 2).
""")

st.divider()

st.subheader("📉 Gráfico de Comportamento Linear")
st.markdown("Simule abaixo como o tempo de banho ($x$) altera o gráfico da função mantendo a torneira ($y$) fixa.")

tempo_fixo_torneira = st.slider("Fixar tempo de torneira aberta para escovação (minutos):", 1, 10, 2)

# Gerando o gráfico da reta f(x) variando o banho de 0 a 30 minutos usando Numpy
x_valores = np.array(range(0, 31))
# Aplica a lei da função
y_valores = (VAZAO_CHUVEIRO * x_valores) + (VAZAO_TORNEIRA_PIA * tempo_fixo_torneira)

fig, ax = plt.subplots(figsize=(6, 3.5))
ax.plot(x_valores, y_valores, label=f"f(x) = {VAZAO_CHUVEIRO}x + {VAZAO_TORNEIRA_PIA * tempo_fixo_torneira}", color="red", linewidth=2.5)
ax.set_xlabel("Tempo de Banho (Minutos) - Eixo X")
ax.set_ylabel("Água Gasta (Litros) - Eixo Y")
ax.set_title("Gráfico da Função de Consumo do Chuveiro", fontsize=11, fontweight='bold')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend()

st.pyplot(fig)
plt.close(fig)

st.success(f"💡 **Conclusão Algébrica:** O gráfico é uma linha reta ascendente. O coeficiente angular ({VAZAO_CHUVEIRO}) determina a inclinação da reta: quanto maior a vazão, mais rápido a reta cresce!")