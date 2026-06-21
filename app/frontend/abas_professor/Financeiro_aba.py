import streamlit as st
from app.backend.database import ler_todos_dados

def renderizar_financeiro():
    st.subheader("💰 Estação Consciência Financeira e Regra de Três")
    
    with st.expander("📚 Ver Aplicação de Porcentagem e Frações"):
        st.markdown("""
        * **Porcentagem como Razão Centesimal:** $30\\% = \\frac{30}{100} = 0,3$
        * **Aplicação na Conta de Água:** Para transformar Litros em Metros Cúbicos ($m^3$), aplicamos uma divisão centesimal/milesimal, sabendo que $1 m^3$ equivale exatamente a $1000$ Litros. 
        * Logo, se uma escola gasta $5000$ Litros, ela consumiu:
        $$\\frac{5000}{1000} = 5 m^3$$
        """)

    df_geral = ler_todos_dados()
    
    tarifa_m3 = st.number_input("Preço da Tarifa do $m^3$ de água local (R$):", min_value=1.0, max_value=30.0, value=6.50, step=0.10)
    
    if df_geral.empty:
        st.warning("Aguardando registros para estimar os impactos financeiros da turma.")
    else:
        litros_totais = df_geral["gasto_total"].sum()
        volume_m3 = litros_totais / 1000.0
        custo_real_total = volume_m3 * tarifa_m3
        
        st.markdown("#### Meta Financeira de Economia Comercial")
        porcentagem_meta = st.slider("Se a escola cortar gastos em quantos por cento (%)?", 10, 50, 25)
        
        economia_dinheiro = custo_real_total * (porcentagem_meta / 100)
        
        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.metric("Volume Geral Coletado", f"{volume_m3:.3f} m³")
        col2.metric("Custo Total da Água", f"R$ {custo_real_total:.2f}")
        col3.metric(f"Economia de Financ. ({porcentagem_meta}%)", f"R$ {economia_dinheiro:.2f}", delta="Poupado")