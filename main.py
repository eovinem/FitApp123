import streamlit as st # type: ignore
import google.generativeai as genai  # type: ignore
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(
    page_title="FitAI - Treino Inteligente",
    page_icon="💪",
    layout="centered"
)

st.title("💪 FitAI - Personal Trainer com Gemini")
st.write("Gere um treino personalizado com base no seu objetivo.")

nome = st.text_input("Seu nome")
idade = st.number_input("Idade", min_value=10, max_value=100)
peso = st.number_input("Peso em kg", min_value=30.0, max_value=200.0)
altura = st.number_input("Altura em cm", min_value=100, max_value=230)

objetivo = st.selectbox(
    "Qual seu objetivo?",
    ["Emagrecer", "Ganhar massa muscular", "Definir o corpo", "Melhorar condicionamento"]
)

nivel = st.selectbox(
    "Seu nível de treino",
    ["Iniciante", "Intermediário", "Avançado"]
)

dias = st.slider("Quantos dias por semana você pode treinar?", 1, 7, 3)
restricoes = st.text_area("Tem alguma lesão ou restrição?")

if st.button("Gerar treino"):
    if not nome:
        st.warning("Digite seu nome.")
    else:
        with st.spinner("Gerando seu treino..."):
            prompt = f"""
            Você é um personal trainer profissional.

            Crie um plano de treino personalizado em português.

            Dados do usuário:
            Nome: {nome}
            Idade: {idade}
            Peso: {peso} kg
            Altura: {altura} cm
            Objetivo: {objetivo}
            Nível: {nivel}
            Dias por semana: {dias}
            Restrições: {restricoes}

            O plano deve conter:
            - Divisão semanal
            - Exercícios por dia
            - Séries e repetições
            - Tempo de descanso
            - Dicas de execução
            - Cuidados importantes
            """

            resposta = model.generate_content(

            )

            st.success("Treino gerado com sucesso!")
            st.markdown(resposta.text)