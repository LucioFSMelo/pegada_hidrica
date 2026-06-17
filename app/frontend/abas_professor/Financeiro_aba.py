import streamlit as st

def renderizar_financeiro():
    st.subheader("💰 Estação Consciência Financeira")
    st.markdown("Transforme o consumo volumétrico de litros de água em valor monetário real em Reais ($R$$).")
    
    # Campo pedagógico para o aluno olhar na conta de água real da sua cidade
    tarifa_m3 = st.number_input("Preço do m³ de água na sua região (R$):", min_value=1.0, max_value=30.0, value=5.50, step=0.10)
    litros_estimados = st.number_input("Digite uma quantidade de litros para simular o custo:", min_value=1, value=1000)
    
    # Conversão matemática: 1 m³ = 1000 Litros
    consumo_m3 = litros_estimados / 1000.0
    custo_total = consumo_m3 * tarifa_m3
    
    st.divider()
    col1, col2 = st.columns(2)
    col1.metric("Volume em Metros Cúbicos", f"{consumo_m3:.3f} m³")
    col2.metric("Custo Estimado", f"R$ {custo_total:.2f}")
    
    st.caption("Fórmula aplicada: $$Custo = \\left(\\frac{\\text{Litros}}{1000}\\right) \\cdot \\text{Tarifa por m}^3$$")