import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# ---- CONFIGURAÇÃO DA PÁGINA ----
st.set_page_config(page_title="Formulário Social Mídia", layout="centered")

st.title("📱 Formulário de Início - Social Mídia")
st.write("Preencha os dados abaixo para começarmos a criar conteúdos incríveis para suas redes!")

# ---- COLETA DE DADOS BÁSICOS ----
nome = st.text_input("Nome completo: ")
profissao = st.text_input("Profissão: ")

# ---- LOGO ----
logo = st.radio("Você já tem uma logo?", ["Sim", "Não"])
detalhes_logo = ""
if logo == "Não":
    detalhes_logo = st.text_area("Como você gostaria da sua logo? (Iniciais, ícone, desenho...)")

# ---- PALETA DE CORES ----
st.write("## Escolha sua paleta de cores")

# Paletas pré-definidas
paletas = {
    "Moderna": ["#1F1F1F", "#E50914", "#F5F5F5"],
    "Elegante": ["#2C3E50", "#ECF0F1", "#8E44AD"],
    "Vibrante": ["#FF6B6B", "#FFD93D", "#6BCB77"],
    "Minimalista": ["#FFFFFF", "#DDDDDD", "#333333"]
}

escolhida = st.radio("Selecione uma paleta de cores:", list(paletas.keys()))

# Mostrar cores visualmente
st.write("### Visualização da paleta:")
cores = paletas[escolhida]
cols = st.columns(len(cores))
for i, cor in enumerate(cores):
    with cols[i]:
        st.markdown(f'<div style="width: 100%%; height: 60px; background-color: {cor}; border: 1px solid #000;"></div>', unsafe_allow_html=True)
        st.caption(cor)

# Opção personalizada
personalizada = st.checkbox("Quero sugerir uma paleta personalizada")
paleta_personalizada = ""
if personalizada:
    paleta_personalizada = st.text_input("Descreva as cores desejadas (ex: tons de azul com detalhes dourados)")

# ---- TIPOS DE CONTEÚDO ----
st.write("## Tipos de conteúdo que você deseja:")
feed = st.checkbox("📷 Feed")
story = st.checkbox("📖 Stories")
reels = st.checkbox("🎬 Reels")

roteiro = ""
if reels:
    roteiro = st.radio("Sobre o Reels:", [
        "Quero que você edite e escreva o roteiro",
        "Eu gravo e você só edita"
    ])

recorrencia = st.selectbox("Com que frequência você quer os posts?", [
    "1x por semana", "2x por semana", "3x por semana", "Diariamente", "Outro"
])

# ---- GERADOR DE PDF ----
def gerar_pdf(dados, nome_arquivo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Informações do Cliente - Social Mídia", ln=True, align="C")
    pdf.ln(10)

    for chave, valor in dados.items():
        texto = f"{chave}: {valor}"
        pdf.multi_cell(0, 10, txt=texto)

    pdf.output(nome_arquivo)

# ---- ENVIO DO FORMULÁRIO ----
if st.button("Enviar formulário"):
    data = datetime.now().strftime("%Y-%m-%d_%H-%M")
    nome_pdf = f"{nome.replace(' ', '')}{data}.pdf"

    dados = {
        "Nome": nome,
        "Profissão": profissao,
        "Tem logo": logo,
        "Detalhes da logo": detalhes_logo,
        "Paleta escolhida": escolhida,
        "Cores da paleta": ", ".join(cores),
        "Paleta personalizada?": "Sim" if personalizada else "Não",
        "Descrição personalizada": paleta_personalizada,
        "Feed": "Sim" if feed else "Não",
        "Stories": "Sim" if story else "Não",
        "Reels": "Sim" if reels else "Não",
        "Roteiro Reels": roteiro,
        "Recorrência": recorrencia
    }

    gerar_pdf(dados, nome_pdf)
    st.success("✅ Formulário enviado e PDF gerado com sucesso!")
    st.download_button("📄 Baixar PDF agora", data=open(nome_pdf, "rb").read(), file_name=nome_pdf, mime="application/pdf")