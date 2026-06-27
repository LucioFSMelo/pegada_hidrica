import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# =====================================================================
# 🧮 TRILHA DE MATEMÁTICA (APROFUNDADA COM GRÁFICOS DINÂMICOS)
# =====================================================================
def renderizar_trilha_matematica():
    st.markdown("### 🧮 Laboratório de Modelagem Matemática e Estatística Social")
    st.write("Ferramentas de análise quantitativa baseadas nas diretrizes da BNCC para modelagem linear, dispersão e correlação socioambiental.")
    
    aba_calc, aba_estat, aba_racismo = st.tabs([
        "💧 Calculadora Multi-variável", 
        "📊 Ranking e Desvio Padrão", 
        "📉 Correlação e Racismo Ambiental"
    ])
    
    with aba_calc:
        st.markdown("#### 1. Matriz de Pegada Hídrica Vetorial (BNCC: EM13MAT302)")
        st.write("Simulação de modelagem matemática baseada no impacto volumétrico de itens cotidianos das cartilhas da Water Footprint Network e Iberdrola.")
        
        col1, col2 = st.columns(2)
        with col1:
            carne = st.slider("Consumo de Carne Bovina (kg/semana):", 0.0, 5.0, 1.5, step=0.1)
            frango = st.slider("Consumo de Frango (kg/semana):", 0.0, 7.0, 2.0, step=0.1)
            cafe = st.slider("Xícaras de Café consumidas (por semana):", 0, 42, 14)
        with col2:
            pizza = st.slider("Pizzas inteiras consumidas (por semana):", 0, 5, 1)
            soja = st.slider("Hambúrguer de Soja (unidades/semana):", 0, 10, 2)
            banho_min = st.slider("Tempo de banho diário (minutos):", 2, 30, 10)

        # Vetor de Consumo Semanal do Usuário (1x6)
        litros_banho_semana = banho_min * 9 * 7  # Média de 9L por minuto
        vetor_consumo = np.array([carne, frango, cafe, pizza, soja, litros_banho_semana])
        
        # Matriz de Fatores de Impacto (6x3): [Pegada Verde, Pegada Azul, Pegada Cinza]
        matriz_fatores = np.array([
            [13000, 1500, 915],   # 1kg Carne Bovina = 15.415L total
            [3500, 500, 325],     # 1kg Frango = 4.325L total
            [120, 7, 3],          # 1 xícara café = 130L total
            [900, 200, 159],      # 1 Pizza = 1.259L total
            [130, 20, 10],        # 1 Hambúrguer Soja = 160L total
            [0, 1, 0]             # Banho Direto: vai 100% para a Pegada Azul
        ])
        
        # Álgebra Linear Básica: Multiplicação Matricial (Vetor 1x6 * Matriz 6x3)
        resultado_pegada = np.dot(vetor_consumo, matriz_fatores)
        verde, azul, cinza = resultado_pegada[0], resultado_pegada[1], resultado_pegada[2]
        total_geral = verde + azul + cinza
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🟢 Pegada Verde (Chuvas)", f"{verde:,.0f} L")
        c2.metric("🔵 Pegada Azul (Rios/Fontes)", f"{azul:,.0f} L")
        c3.metric("⚪ Pegada Cinza (Diluição de Poluentes)", f"{cinza:,.0f} L")
        c4.metric("🔥 Impacto Semanal Total", f"{total_geral:,.0f} L")
        
        # Gráfico de Radar Dinâmico com Plotly
        categorias = ['Pegada Verde', 'Pegada Azul', 'Pegada Cinza']
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[verde, azul, cinza],
            theta=categorias,
            fill='toself',
            name='Sua Pegada',
            line_color='#2980b9'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, max(resultado_pegada) * 1.2])),
            showlegend=False,
            title="Distribuição Multidimensional do Impacto Volumétrico"
        )
        st.plotly_chart(fig_radar, width="stretch")
        
    with aba_estat:
        st.markdown("#### 2. Análise de Dispersão Escolar (BNCC: EM13MAT406)")
        st.write("Análise da discrepância e desigualdade no coeficiente de variação populacional de consumo hídrico.")
        
        # Amostragem simulada para visualização imediata do painel do professor
        np.random.seed(42)
        dados_simulados = pd.DataFrame({
            'Aluno': [f"Aluno {i}" for i in range(1, 21)],
            'Consumo_Total_L': np.random.normal(loc=17500, scale=4000, size=20).round(0)
        })
        dados_simulados.loc[19] = ['Caso Desviante (Outlier)', 31500.0]  # Outlier intencional
        
        media = dados_simulados['Consumo_Total_L'].mean()
        variancia = dados_simulados['Consumo_Total_L'].var()
        desvio_padrao = dados_simulados['Consumo_Total_L'].std()
        coef_variacao = (desvio_padrao / media) * 100
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("📊 Média Amostral", f"{media:,.1f} L")
        m2.metric("📉 Variância Populacional", f"{variancia:,.1f}")
        m3.metric("📐 Desvio Padrão (σ)", f"{desvio_padrao:,.1f} L")
        m4.metric("🔀 Coef. de Variação", f"{coef_variacao:.2f}%")
        
        limite_superior = media + (2 * desvio_padrao)
        outliers = dados_simulados[dados_simulados['Consumo_Total_L'] > limite_superior]
        
        if not outliers.empty:
            for _, row in outliers.iterrows():
                st.error(f"🚨 **Alerta de Discrepância Estrutural:** O usuário **{row['Aluno']}** está operando com {row['Consumo_Total_L']:,.0f} L, ultrapassando a barreira crítica de 2 desvios padrões acima da média!")
        
        fig_disp = px.bar(dados_simulados, x='Aluno', y='Consumo_Total_L', title="Leaderboard de Dispersão de Consumo")
        fig_disp.add_hline(y=media, line_dash="dash", line_color="green", annotation_text="Média Escolar")
        fig_disp.add_hline(y=limite_superior, line_dash="dot", line_color="red", annotation_text="Limite Crítico (2σ)")
        st.plotly_chart(fig_disp, width="stretch")
        
    with aba_racismo:
        st.markdown("#### 3. Correlação Linear de Pearson e Racismo Ambiental (BNCC: EM13MAT106)")
        st.write("Cruzamento de dados demográficos, étnico-raciais e socioeconômicos contra o acesso formal a saneamento básico.")
        
        dados_sociais = pd.DataFrame({
            'Localidade/Bairro': ['Subúrbio Periférico A', 'Favela B', 'Comunidade Central C', 'Conjunto Habitacional D', 'Bairro Centro Nobre', 'Condomínio Continental', 'Zona Alta Periférica', 'Vila Nova'],
            'Renda_Per_Capita_RS': [1100, 700, 650, 1350, 6800, 8000, 780, 950],
            'Populacao_Negra_Parda_Pct': [69, 84, 80, 52, 14, 11, 82, 70],
            'Acesso_Rede_Esgoto_Pct': [40, 15, 18, 65, 100, 100, 10, 35]
        })
        
        st.dataframe(dados_sociais, width="stretch")
        eixo_x = st.selectbox("Selecione a Variável Independente (Eixo X):", ['Renda_Per_Capita_RS', 'Populacao_Negra_Parda_Pct'])
        
        correlacao = dados_sociais[eixo_x].corr(dados_sociais['Acesso_Rede_Esgoto_Pct'])
        
        fig_scatter = px.scatter(
            dados_sociais, x=eixo_x, y='Acesso_Rede_Esgoto_Pct', 
            text='Localidade/Bairro', size='Renda_Per_Capita_RS', trendline="ols",
            title=f"Gráfico de Dispersão: {eixo_x} vs Coleta de Esgoto"
        )
        st.plotly_chart(fig_scatter, width="stretch")
        st.metric("🔗 Coeficiente de Correlação de Pearson (R)", f"{correlacao:.4f}")
        
        if correlacao < -0.6:
            st.warning("⚠️ **Interpretação Matemática:** Há forte correlação linear negativa. Estatisticamente, bairros com maior concentração demográfica de populações pretas e pardas sofrem com menor investimento estrutural em saneamento, caracterizando matematicamente o Racismo Ambiental estrutural.")
        elif correlacao > 0.6:
            st.success("📈 **Interpretação Matemática:** Forte correlação linear positiva. O capital financeiro atua como vetor direto na universalização da infraestrutura hídrica residencial.")

# =====================================================================
# ⚡ TRILHA DE FÍSICA (APROFUNDADA COM SIMULADORES DINÂMICOS)
# =====================================================================
def renderizar_trilha_fisica():
    st.markdown("### ⚡ Laboratório de Termodinâmica e Mecânica dos Fluidos")
    st.write("Exploração prática das leis calorimétricas aplicadas ao consumo doméstico e da física hidrostática na topografia urbana.")
    
    aba_termo, aba_fluidos = st.tabs(["🔥 Termodinâmica do Chuveiro", "🚰 Mecânica dos Fluidos (Stevin)"])
    
    with aba_termo:
        st.markdown("#### 1. Termodinâmica e o Nexo Água-Energia (BNCC: EM13CNT102)")
        st.write("Simulação calorimétrica da equação fundamental da física térmica: $Q = m \\cdot c \\cdot \\Delta\\theta$. Descubra a Pegada Azul Indireta gerada pela evaporação hídrica nos reservatórios das hidrelétricas.")
        
        col1, col2 = st.columns(2)
        with col1:
            vazao = st.slider("Vazão Hidráulica (Litros por minuto):", 3.0, 15.0, 8.0, step=0.5)
            tempo = st.slider("Tempo de Uso (minutos):", 2, 30, 10)
        with col2:
            t_inicial = st.slider("Temperatura de Entrada da Água (°C):", 10, 25, 16)
            t_final = st.slider("Temperatura de Saída no Chuveiro (°C):", 30, 45, 38)
            
        c_agua = 4186  # Calor específico da água: J/(kg*°C)
        massa_agua = vazao * tempo * 1.0  # Densidade da água = 1 kg/L
        delta_t = t_final - t_inicial
        
        energia_joules = massa_agua * c_agua * delta_t
        energia_kwh = energia_joules / 3600000  # 1 kWh = 3.6 x 10^6 J
        
        custo_luz = energia_kwh * 0.85  # Média de tarifa por kWh
        custo_agua = massa_agua * 0.006  # Tarifa volumétrica simulada
        
        # Impacto Invisível: Hidrelétricas perdem cerca de 4 litros de água por evaporação por kWh gerado
        evaporacao_indireta = energia_kwh * 4.0
        
        f1, f2, f3 = st.columns(3)
        f1.metric("⚡ Trabalho Térmico Calculado", f"{energia_kwh:.2f} kWh")
        f2.metric("💸 Despesa Integrada (Água + Luz)", f"R$ {(custo_luz + custo_agua):.2f}")
        f3.metric("💧 Pegada Azul Indireta (Usina)", f"{evaporacao_indireta:.1f} Litros")
        
        fig_nexo = go.Figure(data=[
            go.Bar(name='Água Direta Consumida (L)', x=['Matriz de Impacto'], y=[massa_agua], marker_color='#3498db'),
            go.Bar(name='Água Indireta Evaporada na Usina (L)', x=['Matriz de Impacto'], y=[evaporacao_indireta], marker_color='#f39c12')
        ])
        fig_nexo.update_layout(barmode='group', title="O Nexo Oculto entre Água e Energia Elétrica")
        st.plotly_chart(fig_nexo, width="stretch")
        
    with aba_fluidos:
        st.markdown("#### 2. Teorema de Stevin e a Desigualdade de Pressão Hidrostática ($p = d \\cdot g \\cdot h$)")
        st.write("Compreenda graficamente como a variação da altura geométrica ($h$) dita a pressão nos canos e pune assentamentos em cotas topográficas elevadas.")
        
        altura_reservatorio = st.slider("Cota Altométrica do Reservatório Central da Cidade (metros):", 20, 100, 60)
        
        pontos_cidade = pd.DataFrame({
            'Localidade': ['Bairro Baixo / Centro', 'Zona Comercial Central', 'Periferia Plana', 'Favela em Morro Alto'],
            'Altitude_Meters': [12, 18, 28, 56]
        })
        
        g = 9.81
        d_agua = 1000  # kg/m³
        pressões_kpa = []
        alertas = []
        
        for _, local in pontos_cidade.iterrows():
            h_hidro = altura_reservatorio - local['Altitude_Meters']
            if h_hidro <= 0:
                p_kpa = 0.0
                status = "❌ Desabastecimento Total (Cota Incompatível)"
            else:
                p_pascal = d_agua * g * h_hidro
                p_kpa = p_pascal / 1000
                status = "⚠️ Pressão Crítica (Risco de Intermitência)" if p_kpa < 100 else "✅ Fluxo e Pressão Normais"
            pressões_kpa.append(p_kpa)
            alertas.append(status)
            
        pontos_cidade['Pressao_kPa'] = pressões_kpa
        pontos_cidade['Status_Rede'] = alertas
        
        st.dataframe(pontos_cidade, width="stretch")
        
        fig_topo = go.Figure()
        fig_topo.add_trace(go.Scatter(
            x=pontos_cidade['Localidade'], y=pontos_cidade['Altitude_Meters'],
            mode='lines+markers+text', text=pontos_cidade['Status_Rede'],
            textposition="top center", name='Corte do Terreno', fill='tozeroy', line_color='#e67e22'
        ))
        fig_topo.add_hline(y=altura_reservatorio, line_dash="dash", line_color="blue", annotation_text="Nível de Carga do Reservatório")
        fig_topo.update_layout(title="Perfil Topográfico e Linha de Pressão Estática Piezométrica", yaxis_title="Altitude (m)")
        st.plotly_chart(fig_topo, width="stretch")

# =====================================================================
# ✍️ TRILHA DE LÍNGUA PORTUGUESA
# =====================================================================
def renderizar_trilha_portugues():
    st.markdown("### ✍️ Laboratório de Língua Portuguesa e Análise de Discurso")
    aba_disc, aba_red = st.tabs(["🔎 Raio-X do Discurso", "📝 Lab de Argumentação (ENEM)"])
    
    with aba_disc:
        st.markdown("#### 1. Análise Crítica e Ideológica do Léxico (BNCC: EM13LP01)")
        texto_analise = "A universalização mitigará o deficit técnico de infraestrutura hídrica periférica, superando a morosidade do Estado e o histórico Racismo Ambiental."
        st.text_area("Enunciado em Análise Coletiva:", texto_analise, height=70, disabled=True)
        
        termo = st.selectbox("Selecione um termo para quebrar sua estrutura ideológica:", ["Selecione...", "Universalização", "Deficit técnico", "Racismo Ambiental"])
        if termo == "Universalização":
            st.info("Conceito do Marco Legal do Saneamento. Politicamente amarra a promessa de acesso total à privatização e à concessão de ativos hídricos.")
        elif termo == "Deficit técnico":
            st.warning("Eufemismo burocrático. Reduz escolhas políticas e a exclusão social deliberada a meros problemas logísticos ou falta de encanamentos.")
        elif termo == "Racismo Ambiental":
            st.error("Léxico Crítico. Denuncia a distribuição racialmente desigual dos ônus da degradação ambiental e da ausência deliberada de infraestrutura básica.")

    with aba_red:
        st.markdown("#### 2. Laboratório Crítico de Redação")
        st.text_input("Tese Central:")
        st.text_area("Desenvolvimento Argumentativo (Incorporate Termodinâmica ou Stevin):")
        st.text_input("Intervenção Social (Competência 5 ENEM):")
        st.button("Mapear Conectivos e Coesão")

# =====================================================================
# 🌍 TRILHA DE GEOGRAFIA (NORDESTE: RELEVO E HIDROGRAFIA)
# =====================================================================
def renderizar_trilha_geografia():
    st.markdown("### 🌍 Laboratório de Geopolítica e Análise Espacial (GIS)")
    aba_nordeste, aba_virtual = st.tabs(["🗺️ Relevo e Hidrografia do Nordeste", "🌐 Água Virtual"])
    
    with aba_nordeste:
        st.markdown("#### 1. Geofísica e Climatologia do Semiarid (BNCC: EM13CHS204)")
        st.write("Estudo do Polígono das Secas, da dinâmica geomorfológica e da perenidade dos rios do Nordeste.")
        
        st.markdown("""
        * **O Bloqueio Orográfico do Relevo:** O **Planalto da Borborema** atua como barreira física às massas úmidas oceânicas. O ar sobe, resfria e chove no agreste/litoral, descendo seco e aquecido sobre a **Depressão Sertaneja** (efeito Sombra de Chuva).
        * **Rios Intermitentes vs Perenes:** A evapotranspiração acelerada torna os rios sazonais ou intermitentes (secam no estio). O **Rio São Francisco** e o **Rio Parnaíba** destacam-se como artérias perenes fundamentais, alimentadas por cabeceiras exógenas e úmidas.
        * **A Transposição do Velho Chico:** Geopolítica da água. Canais artificiais mudam o rumo hídrico do Nordeste para mitigar colapsos em bacias receptoras, dividindo opiniões entre o abastecimento humano difuso e o atendimento do agronegócio de exportação.
        """)
        
        fig_nordeste = go.Figure(data=[go.Scatter(
            x=['Zona da Mata / Litoral', 'Planalto da Borborema', 'Depressão Sertaneja (Interior)'],
            y=[0, 850, 180], mode='lines+markers+text',
            text=['Umidade Barrada', 'Ascensão Orográfica', 'Ar Seco (Sertão)'],
            textposition="top center", fill='tozeroy', line_color='#8B4513'
        )])
        fig_nordeste.update_layout(title="Perfil Topográfico Esquemático Clima-Relevo Nordestino", yaxis_title="Altitude (m)")
        st.plotly_chart(fig_nordeste, width="stretch")

    with aba_virtual:
        st.markdown("#### 2. Fluxo Comercial Invisível de Água Doce")
        prod = st.selectbox("Commodity de Rastreamento de Rota:", ["1 Tonelada de Soja do Cerrado", "1kg de Carne Bovina"])
        if prod == "1 Tonelada de Soja do Cerrado":
            st.info("🚢 **Fluxo de Água Virtual:** Cerca de 1.700.000 Litros de água invisível viajam embutidos nos grãos até portos chineses ou europeus. Ocorre uma transferência ecológica de estresse hídrico oculto.")
        else:
            st.info("🚢 **Fluxo de Água Virtual:** São necessários 15.415 Litros de água reais (entre pasto, grãos e processamento animal) para viabilizar 1kg de carne para exportação global.")

# =====================================================================
# 🔬 TRILHA DE CIÊNCIAS, BIOLOGIA E QUÍMICA
# =====================================================================
def renderizar_trilha_ciencias():
    st.markdown("### 🔬 Laboratório de Ciclos Biogeoquímicos e Saneamento Químico")
    aba_eutrof, aba_eta = st.tabs(["🦠 Eutrofização Virtual", "🧪 Operação da ETA"])
    
    with aba_eutrof:
        st.markdown("#### 1. Ciclos do Nitrogênio e Fósforo (BNCC: EM13CNT302)")
        carga = st.select_slider("Lançamento de Nitratos e Fosfatos (Esgoto Doméstico ou Fertilizante):", options=["Preservado", "Carga Moderada", "Carga Orgânica Crítica"])
        
        if carga == "Preservado":
            st.success("🟢 Oxigênio Dissolvido (OD) ideal (~8 mg/L). Água límpida. Fauna e flora em equilíbrio homeostático estável.")
        elif carga == "Carga Moderada":
            st.warning("🟡 Multiplicação inicial de algas microscópicas na camada fótica. Redução gradual de luminosidade profunda.")
        else:
            st.error("🔴 **Colapso de Pegada Cinza:** Hiperproliferação de cianobactérias bloqueia 100% da luz solar. A fotossíntese de plantas de fundo cessa. A decomposição aeróbica da biomassa morta esgota o Oxigênio Dissolvido (OD -> 0 mg/L), asfixiando os peixes em massa.")

    with aba_eta:
        st.markdown("#### 2. Filtro Virtual de Saneamento Mecânico-Químico")
        st.write("Ordene as etapas operacionais da Estação de Tratamento de Água (ETA):")
        p1 = st.selectbox("Fase I:", ["Coagulação / Floculação (Sulfato de Alumínio)", "Decantação", "Filtração", "Cloração e Fluoretação"])
        p2 = st.selectbox("Fase II:", ["Coagulação / Floculação", "Decantação", "Filtração", "Cloração e Fluoretação"])
        p3 = st.selectbox("Fase III:", ["Coagulação / Floculação", "Decantação", "Filtração", "Cloração e Fluoretação"])
        p4 = st.selectbox("Fase IV:", ["Coagulação / Floculação", "Decantação", "Filtração", "Cloração e Fluoretação"])
        
        if st.button("Acionar Válvulas da ETA"):
            if p1.startswith("Coagulação") and p2 == "Decantação" and p3 == "Filtração" and p4.startswith("Cloração"):
                st.success("🎯 **Perfeito!** O tratamento químico seguiu o rigor termodinâmico e mecânico. Sujeira aglutinada, precipitada, retida e patógenos erradicados.")
            else:
                st.error("❌ **Erro de Processo:** A água chegou turva ou contaminada à rede de distribuição urbana.")