import streamlit as st
import random

st.set_page_config(page_title="Quiz da Água", page_icon="🧠", layout="centered")

# Banco de 20 questões dinâmicas
BANCO_QUESTOES = [
    {"q": "1 m³ (metro cúbico) equivale a quantos litros?", "opcoes": ["10", "100", "1.000", "10.000"], "correta": "1.000"},
    {"q": "Como as companhias de água cobram a conta?", "opcoes": ["Em Litros", "Em Metros Cúbicos (m³)", "Em Quilogramas", "Em Mililitros"], "correta": "Em Metros Cúbicos (m³)"},
    {"q": "A maior parte da água doce do mundo é gasta em qual setor?", "opcoes": ["Residencial", "Indústria", "Agropecuária", "Comércio"], "correta": "Agropecuária"},
    {"q": "Qual a porcentagem de água doce acessível no planeta?", "opcoes": ["Aproximadamente 1%", "Cerca de 25%", "Mais de 50%", "Quase 97%"], "correta": "Aproximadamente 1%"},
    {"q": "Fechar a torneira ao escovar os dentes reduz o fluxo de água em até:", "opcoes": ["10%", "50%", "70%", "90%"], "correta": "90%"}, # Pois gasta 10%
    {"q": "Um banho de 10 min gasta cerca de quantos litros se não fecharmos o chuveiro (vazão 15L/min)?", "opcoes": ["50 Litros", "100 Litros", "150 Litros", "200 Litros"], "correta": "150 Litros"},
    {"q": "A água que não vemos, usada para produzir alimentos e roupas, chama-se:", "opcoes": ["Água Cinza", "Água Virtual (Pegada Hídrica)", "Água Negra", "Água Subterrânea"], "correta": "Água Virtual (Pegada Hídrica)"},
    {"q": "O que indica vazamento em um hidrômetro?", "opcoes": ["Rodízio vermelho girando sem água aberta", "Números pretos parados", "Água transparente", "Ponteiro não se move"], "correta": "Rodízio vermelho girando sem água aberta"},
    {"q": "Quantos litros são gastos, em média, para produzir 1 kg de carne bovina?", "opcoes": ["15 Litros", "150 Litros", "1.500 Litros", "Mais de 15.000 Litros"], "correta": "Mais de 15.000 Litros"},
    {"q": "Uma torneira gotejando pode desperdiçar por dia cerca de:", "opcoes": ["1 Litro", "5 Litros", "40 a 50 Litros", "100 Litros"], "correta": "40 a 50 Litros"},
    {"q": "Para produzir 1 calça jeans, a pegada hídrica média é:", "opcoes": ["100 Litros", "500 Litros", "1.000 Litros", "Cerca de 10.000 Litros"], "correta": "Cerca de 10.000 Litros"},
    {"q": "O Aquífero Guarani, um dos maiores do mundo, fica principalmente no:", "opcoes": ["Deserto do Saara", "Continente Asiático", "América do Sul", "América do Norte"], "correta": "América do Sul"},
    {"q": "No ciclo da água, a transformação do vapor em nuvens chama-se:", "opcoes": ["Evaporação", "Condensação", "Precipitação", "Infiltração"], "correta": "Condensação"},
    {"q": "Água de reuso (água cinza) é adequada para:", "opcoes": ["Beber", "Cozinhar", "Lavar calçadas e dar descarga", "Tomar banho"], "correta": "Lavar calçadas e dar descarga"},
    {"q": "Se uma torneira vaza 6 litros por minuto, em 1 hora gastará:", "opcoes": ["60 Litros", "160 Litros", "360 Litros", "600 Litros"], "correta": "360 Litros"},
    {"q": "O bioma brasileiro conhecido como 'Caixa d'água do Brasil' é o:", "opcoes": ["Cerrado", "Caatinga", "Amazônia", "Pampa"], "correta": "Cerrado"},
    {"q": "Qual eletrodoméstico geralmente consome mais água em uma residência?", "opcoes": ["Geladeira", "Máquina de Lavar Roupas", "Filtro de Água", "Micro-ondas"], "correta": "Máquina de Lavar Roupas"},
    {"q": "Desmatamento nas margens de rios causa um problema chamado:", "opcoes": ["Assoreamento", "Evaporação", "Infiltração", "Ebulição"], "correta": "Assoreamento"},
    {"q": "Área de floresta nativa protegida ao redor de rios e nascentes:", "opcoes": ["Mata Ciliar (APP)", "Reserva de Extração", "Pastagem", "Área Urbana"], "correta": "Mata Ciliar (APP)"},
    {"q": "A principal lei brasileira que gerencia as águas é a:", "opcoes": ["Lei do Trânsito", "Política Nacional de Recursos Hídricos", "Estatuto da Criança", "Lei Trabalhista"], "correta": "Política Nacional de Recursos Hídricos"}
]

# Inicializa as variáveis de jogo
if 'quiz_rodada' not in st.session_state:
    st.session_state.quiz_rodada = random.sample(BANCO_QUESTOES, 5) # Sorteia 5
    st.session_state.questao_atual = 0
    st.session_state.pontuacao = 0
    st.session_state.quiz_finalizado = False

st.title("🧠 O Grande Quiz da Água")

if not st.session_state.quiz_finalizado:
    # Mostra a pergunta atual
    idx = st.session_state.questao_atual
    pergunta = st.session_state.quiz_rodada[idx]
    
    st.markdown(f"### Pergunta {idx + 1} de 5:")
    st.write(pergunta["q"])
    
    # Cria os botões com formatação
    resposta_escolhida = st.radio("Selecione sua resposta:", pergunta["opcoes"], index=None)
    
    if st.button("Confirmar Resposta"):
        if resposta_escolhida:
            if resposta_escolhida == pergunta["correta"]:
                st.session_state.pontuacao += 1
                st.success("✅ Resposta Correta!")
            else:
                st.error(f"❌ Incorreto. A certa era: {pergunta['correta']}")
            
            # Avança a pergunta
            st.session_state.questao_atual += 1
            if st.session_state.questao_atual >= 5:
                st.session_state.quiz_finalizado = True
            st.rerun() # Atualiza a tela
        else:
            st.warning("Selecione uma opção antes de confirmar!")

else:
    # Tela Final
    st.balloons()
    st.header("🏆 Quiz Concluído!")
    st.metric("Sua Pontuação Final", f"{st.session_state.pontuacao} de 5 acertos")
    
    if st.session_state.pontuacao == 5:
        st.success("Mestre da Sustentabilidade! Gabaritou!")
    elif st.session_state.pontuacao >= 3:
        st.info("Muito bom! Mas ainda dá para melhorar.")
    else:
        st.warning("Precisamos estudar mais os recursos hídricos!")
        
    if st.button("🔄 Jogar Novamente (Sortear Novas Perguntas)"):
        del st.session_state.quiz_rodada
        st.rerun()