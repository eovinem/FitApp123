import streamlit as st # type: ignore
import google.generativeai as genai  # type: ignore
from dotenv import load_dotenv # type: ignore
from database import criar_banco
import sqlite3
import os

load_dotenv()
criar_banco()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


try:
     resposta = model.generate_content(prompt)

     st.success("Treino gerado com sucesso!")
     st.session_state["Ultimo treino"] = resposta.text
     st.markdown(st.session_state["Ultimo treino"].replace("\n", "<br>"), unsafe_allow_html=True)


except Exception as e:
    st.error(f"Limite temporário da IA atingido. Aguarde e tente novamente. {str(e)}")

st.set_page_config(        
    page_title="FitAI - Treino Inteligente",
    page_icon="💪",
    layout="centered"
)

if "Ultimo treino" not in st.session_state:
        st.session_state["Ultimo treino"] = None,


st.markdown("""
<style>
.stApp {
            background-color:#0b0f0d;
            color: white;
}
    [data-testid="stSidebar"]{
    background-color: #111714
                    
}
            
.card{
    background-color: #151c18
    padding: 20px 
    border-radius: 16px
    border: 1px solid #1f2b24
    margin-bottom: 16px;
     
}
.grenn-title {
    color: #39dd8;
    font-size:20px;
    font-weight: 700px;        
            
}
</style>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Menu",

    [
        "🏠 Dashboard",
        "💪 Gerar Treino",
        "⚖️ IMC",
        "📜 Histórico"
    ]
)


st.title("🏋️ FitAI")
st.caption("Seu treinador pessoal inteligente")
st.write("Crie um treino personalizado de acordo com seu ojetivo.")

nome = st.text_input("Seu nome")
idade = st.number_input("Idade", min_value=10, max_value=100)
peso = st.number_input("Peso em kg", min_value=30.0, max_value=200.0)
altura = st.number_input("Altura em cm", min_value=100, max_value=230)

if altura > 0:
    imc = peso / ((altura / 100)** 2)

    if imc < 18.5:
        classificacao = "Você está abaixo do peso"

    elif imc < 25:
        classificacao = "Você está no peso ideial"
    
    elif imc < 30:
        classificacao = "Você está Sobrepeso"

    else:
        classificacao = "Você possui Obesidade"

    st.metric("Seu IMC", f"{imc:.1f}")
    st.info(f"Classificação: {classificacao}")


objetivo = st.selectbox(
    "Qual seu objetivo?",
    [
        "Emagrecer",
        "Ganhar massa muscular",
        "Melhorar condicionamento"        

    ]
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
            - Objetivo
            - Nível
            - Dias por semana
            
            Treino:

            Dia 1:
            - Exercício | Séries | Repetições 

            Dia 2:
            - Exercício | Séries | Repetições 

            Regras:
            - Máximo 300 palavras.
            - Não explique exercícios.
            - Não escreva introduções. 
            - Não inclua plano alimentar.
            """

            resposta = model.generate_content(prompt)

            

            st.success("Treino gerado com sucesso!")
            st.session_state["Ultimo treino"] = resposta.text
            st.markdown(st.session_state["Ultimo treino"].replace("\n", "<br>"), unsafe_allow_html=True)

            conn = sqlite3.connect("fitai.db")
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO treinos
            (nome, objetivo, imc, treino)
            VALUES (?, ?, ?, ?)
            """, (
                nome,
                objetivo,
                round(imc, 1,),
                resposta.text
            ))

            conn.commit()
            conn.close()

if menu == "📜 Histórico":
        
        st.title("📜 Histórico")
        conn = sqlite3.connect("fitai.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT nome, objetivo, imc, treino, data
        FROM treinos
        ORDER BY data DESC
        """)
        resultados = cursor.fetchall()
        conn.close()

        for row in resultados:
            st.write(f"**{row[0]}** - {row[1]}")
            st.write(f"IMC: {row[2]}")
            st.write(f"Treino: {row[3]}")
            st.write(f"Data: {row[4]}")
            st.divider()


        if st.session_state["Ultimo treino"]:
            st.title("Último treino gerado")
            st.markdown(st.session_state["Ultimo treino"].replace("\n", "<br>"), unsafe_allow_html=True)
        else:
            st.info("Nenhum treino gerado ainda.")