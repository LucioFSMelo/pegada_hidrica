import streamlit as st
import random

st.set_page_config(page_title="Quiz da Água", page_icon="🧠", layout="centered")

# Banco de 20 questões dinâmicas com explicações pedagógicas integradas
BANCO_QUESTOES = [
    {
        "q": "1 m³ (metro cúbico) equivale a quantos litros?", 
        "opcoes": ["10", "100", "1.000", "10.000"], 
        "correta": "1.000",
        "explicacao": "Conversão fundamental de unidades de volume: 1 metro cúbico comporta exatamente 1.000 litros de água."
    },
    {
        "q": "Como as companhias de água cobram a conta?", 
        "opcoes": ["Em Litros", "Em Metros Cúbicos (m³)", "Em Quilogramas", "Em Mililitros"], 
        "correta": "Em Metros Cúbicos (m³)",
        "explicacao": "A leitura do hidrômetro registra o volume consumido em metros cúbicos (m³). Cada 1 m³ na conta representa 1.000 litros faturados."
    },
    {
        "q": "A maior parte da água doce do mundo é gasta em qual setor?", 
        "opcoes": ["Residencial", "Indústria", "Agropecuária", "Comércio"], 
        "correta": "Agropecuária",
        "explicacao": "Segundo dados globais, a irrigação e a agropecuária respondem por cerca de 70% de todo o consumo de água doce do planeta."
    },
    {
        "q": "Qual a porcentagem de água doce acessível no planeta?", 
        "opcoes": ["Aproximadamente 1%", "Cerca de 25%", "Mais de 50%", "Quase 97%"], 
        "correta": "Aproximadamente 1%",
        "explicacao": "Embora a Terra seja coberta por água, 97% é salgada. Dos 3% de água doce, a maior parte está congelada em geleiras, restando apenas cerca de 1% acessível para consumo humano."
    },
    {
        "q": "Fechar a torneira ao escovar os dentes reduz o fluxo de água em até:", 
        "opcoes": ["10%", "50%", "70%", "90%"], 
        "correta": "90%",
        "explicacao": "Ao fechar a torneira enquanto escova os dentes, você usa a água apenas para molhar e enxaguar, gerando uma economia de até 90% em relação a deixar a torneira aberta o tempo todo."
    },
    {
        "q": "Um banho de 10 min gasta cerca de quantos litros se não fecharmos o chuveiro (vazão 15L/min)?", 
        "opcoes": ["50 Litros", "100 Litros", "150 Litros", "200 Litros"], 
        "correta": "150 Litros",
        "explicacao": "Usando a Fórmula do Detetive (Tempo x Vazão): 10 minutos x 15 L/min = 150 Litros de água consumidos."
    },
    {
        "q": "A água que não vemos, usada para produzir alimentos e roupas, chama-se:", 
        "opcoes": ["Água Cinza", "Água Virtual (Pegada Hídrica)", "Água Negra", "Água Subterrânea"], 
        "correta": "Água Virtual (Pegada Hídrica)",
        "explicacao": "Água Virtual representa o volume de água embutido no processo de fabricação e cadeia produtiva de tudo o que consumimos."
    },
    {
        "q": "O que indica vazamento em um hidrômetro?", 
        "opcoes": ["Rodízio vermelho girando sem água aberta", "Números pretos parados", "Água transparente", "Ponteiro não se move"], 
        "correta": "Rodízio vermelho girando sem água aberta",
        "explicacao": "Se todas as torneiras da casa estão fechadas e o indicador circular (rodízio) continua girando, significa que a água está fluindo para algum vazamento invisível."
    },
    {
        "q": "Quantos litros são gastos, em média, para produzir 1 kg de carne bovina?", 
        "opcoes": ["15 Litros", "150 Litros", "1.500 Litros", "Mais de 15.000 Litros"], 
        "correta": "Mais de 15.000 Litros",
        "explicacao": "A pegada hídrica da carne bovina é altíssima devido à água consumida pelo animal ao longo da vida e à produção de grãos para sua ração."
    },
    {
        "q": "Uma torneira gotejando pode desperdiçar por dia cerca de:", 
        "opcoes": ["1 Litro", "5 Litros", "40 a 50 Litros", "100 Litros"], 
        "correta": "40 a 50 Litros",
        "explicacao": "Pequenos gotejamentos constantes agem como um ralo financeiro e ecológico, totalizando cerca de 46 litros desperdiçados a cada 24 horas."
    },
    {
        "q": "Para produzir 1 calça jeans, a pegada hídrica média é:", 
        "opcoes": ["100 Litros", "500 Litros", "1.000 Litros", "Cerca de 10.000 Litros"], 
        "correta": "Cerca de 10.000 Litros",
        "explicacao": "Desde o cultivo intensivo de algodão até o tingimento industrial do tecido, uma única calça jeans demanda milhares de litros de água doce."
    },
    {
        "q": "O Aquífero Guarani, um dos maiores do mundo, fica principalmente no:", 
        "opcoes": ["Deserto do Saara", "Continente Asiático", "América do Sul", "América do Norte"], 
        "correta": "América do Sul",
        "explicacao": "O Aquífero Guarani é um gigantesco reservatório subterrâneo de água doce localizado no subsolo do Brasil, Argentina, Paraguai e Uruguai."
    },
    {
        "q": "No ciclo da água, a transformação do vapor em nuvens chama-se:", 
        "opcoes": ["Evaporação", "Condensação", "Precipitação", "Infiltração"], 
        "correta": "Condensação",
        "explicacao": "Condensação é a mudança do estado gasoso para o líquido. O vapor quente sobe, esfria na atmosfera e forma gotículas que criam as nuvens."
    },
    {
        "q": "Água de reuso (água cinza) é adequada para:", 
        "opcoes": ["Beber", "Cozinhar", "Lavar calçadas e dar descarga", "Tomar banho"], 
        "correta": "Lavar calçadas e dar descarga",
        "explicacao": "A água cinza provém do chuveiro ou máquina de lavar. Não serve para ingestão ou higiene, mas é perfeita para atividades secundárias de limpeza e escoamento sanitário."
    },
    {
        "q": "Se uma torneira vaza 6 litros por minuto, em 1 hora gastará:", 
        "opcoes": ["60 Litros", "160 Litros", "360 Litros", "600 Litros"], 
        "correta": "360 Litros",
        "explicacao": "Modelagem matemática elementar: Como 1 hora possui 60 minutos, calculamos 6 Litros x 60 minutos = 360 Litros."
    },
    {
        "q": "O bioma brasileiro conhecido como 'Caixa d'água do Brasil' é o:", 
        "opcoes": ["Cerrado", "Caatinga", "Amazônia", "Pampa"], 
        "correta": "Cerrado",
        "explicacao": "O Cerrado recebe esse título pois abriga as nascentes de importantes bacias hidrográficas que abastecem o país e geram energia hidroelétrica."
    },
    {
        "q": "Qual eletrodoméstico geralmente consome mais água em uma residência?", 
        "opcoes": ["Geladeira", "Máquina de Lavar Roupas", "Filtro de Água", "Micro-ondas"], 
        "correta": "Máquina de Lavar Roupas",
        "explicacao": "Ciclos completos de lavagem de roupas demandam um volume massivo de água, tornando o eletrodoméstico o campeão de consumo interno."
    },
    {
        "q": "Desmatamento nas margens de rios causa um problema chamado:", 
        "opcoes": ["Assoreamento", "Evaporação", "Infiltração", "Ebulição"], 
        "correta": "Assoreamento",
        "explicacao": "Sem as raízes da mata ciliar para segurar a terra, a chuva empurra o solo para dentro do leito do rio, diminuindo sua profundidade e sufocando o curso da água."
    },
    {
        "q": "Área de floresta nativa protegida ao redor de rios e nascentes:", 
        "opcoes": ["Mata Ciliar (APP)", "Reserva de Extração", "Pastagem", "Área Urbana"], 
        "correta": "Mata Ciliar (APP)",
        "explicacao": "A Mata Ciliar é considerada Área de Preservação Permanente (APP) por agir como cílios protegendo os olhos d'água contra erosões e contaminações."
    },
    {
        "q": "A principal lei brasileira que gerencia as águas é a:", 
        "opcoes": ["Lei do Trânsito", "Política Nacional de Recursos Hídricos", "Estatuto da Criança", "Lei Trabalhista"], 
        "correta": "Política Nacional de Recursos Hídricos",
        "explicacao": "Instituída pela Lei nº 9.433/1997 (conhecida como Lei das Águas), ela dita que a água é um bem público, limitado e dotado de valor econômico."
    }
]

# Inicializa as variáveis de jogo de forma robusta
if 'quiz_rodada' not in st.session_state:
    st.session_state.quiz_rodada = random.sample(BANCO_QUESTOES, 5) # Sorteia 5 dinamicamente
    st.session_state.questao_atual = 0
    st.session_state.pontuacao = 0
    st.session_state.quiz_finalizado = False
    st.session_state.respondido = False
    st.session_state.resposta_salva = None

st.title("🧠 O Grande Quiz da Água")

if not st.session_state.quiz_finalizado:
    idx = st.session_state.questao_atual
    pergunta = st.session_state.quiz_rodada[idx]
    
    st.markdown(f"### Pergunta {idx + 1} de 5:")
    st.markdown(f"#### **{pergunta['q']}**")
    
    # Se o aluno já respondeu, desabilita as opções para ele não trapacear antes de ir para a próxima
    resposta_escolhida = st.radio(
        "Selecione sua resposta:", 
        pergunta["opcoes"], 
        index=None if not st.session_state.respondido else pergunta["opcoes"].index(st.session_state.resposta_salva),
        disabled=st.session_state.respondido,
        key=f"radio_q_{idx}"
    )
    
    st.divider()
    
    # Fluxo em Dois Tempos: Tempo 1 (Confirmar), Tempo 2 (Avançar)
    if not st.session_state.respondido:
        if st.button("Confirmar Resposta", use_container_width=True):
            if resposta_escolhida:
                st.session_state.respondido = True
                st.session_state.resposta_salva = resposta_escolhida
                if resposta_escolhida == pergunta["correta"]:
                    st.session_state.pontuacao += 1
                st.rerun()
            else:
                st.warning("⚠️ Selecione uma opção antes de confirmar!")
    else:
        # Apresentação do Veredito Pedagógico
        if st.session_state.resposta_salva == pergunta["correta"]:
            st.success(f"🎯 **Resposta Correta!** Você marcou: {pergunta['correta']}")
        else:
            st.error(f"❌ **Incorreto.** Você marcou '{st.session_state.resposta_salva}'. A alternativa certa era: {pergunta['correta']}")
            
        # Exibição da Explicação com base nos arquivos didáticos fornecidos
        st.info(f"💡 **Explicação Detetive:** {pergunta['explicacao']}")
        
        # Botão para ir de fato ao próximo elemento
        if st.button("Próxima Pergunta ➡️", use_container_width=True):
            st.session_state.questao_atual += 1
            st.session_state.respondido = False
            st.session_state.resposta_salva = None
            
            if st.session_state.questao_atual >= 5:
                st.session_state.quiz_finalizado = True
            st.rerun()

else:
    # Tela Final de Resultados Consolidados
    st.balloons()
    st.header("🏆 Quiz Concluído!")
    st.metric("Sua Pontuação Final", f"{st.session_state.pontuacao} acertos de 5 perguntas")
    
    # Mensagens de Feedback Orientado por Faixa de Desempenho
    if st.session_state.pontuacao == 5:
        st.success("🟢 Mestre da Sustentabilidade! Você gabaritou e provou ser um verdadeiro Detetive da Água!")
    elif st.session_state.pontuacao >= 3:
        st.info("🔵 Muito bom! Demonstrou grande conhecimento, mas revise os materiais para ficar impecável.")
    else:
        st.warning("⚠️ Precisamos estudar mais os recursos hídricos! Baixe o guia na Home e tente de novo.")
        
    if st.button("🔄 Jogar Novamente (Sortear Novas Perguntas)"):
        # Limpa o cache específico da rodada para que o random.sample rode de novo
        del st.session_state.quiz_rodada
        st.session_state.questao_atual = 0
        st.session_state.pontuacao = 0
        st.session_state.quiz_finalizado = False
        st.session_state.respondido = False
        st.session_state.resposta_salva = None
        st.rerun()