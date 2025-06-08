import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# ---- CONFIGURAÇÃO DA PÁGINA ----
st.set_page_config(page_title="Formulário Social Mídia", layout="centered")

st.title("📱 Formulário de Início - Social Mídia")
st.write("Preencha os dados abaixo para começarmos a criar conteúdos incríveis para suas redes!")

# ---- COLETA DE DADOS BÁSICOS ----
nome = st.text_input("Nome completo")
profissao = st.text_input("Profissão")

# ---- LOGO ----
logo = st.radio("Você já tem uma logo?", ["Sim", "Não"])
detalhes_logo = ""
if logo == "Não":
    detalhes_logo = st.text_area("Como você gostaria da sua logo? (Iniciais, ícone, desenho...)")

# ---- PALETA DE CORES INTERATIVA ----
st.write("## Escolha sua paleta de cores")

# Dicionário das cores base e seus tons (hex)
cores_base = {
    "Vermelho": ["#FFCDD2", "#EF9A9A", "#E57373", "#EF5350", "#F44336", "#D32F2F", "#B71C1C"],
    "Azul": ["#BBDEFB", "#90CAF9", "#64B5F6", "#42A5F5", "#2196F3", "#1976D2", "#0D47A1"],
    "Verde": ["#C8E6C9", "#A5D6A7", "#81C784", "#66BB6A", "#4CAF50", "#388E3C", "#1B5E20"],
    "Amarelo": ["#FFF9C4", "#FFF59D", "#FFF176", "#FFEE58", "#FFEB3B", "#FBC02D", "#F57F17"],
    "Marrom": ["#D7CCC8", "#BCAAA4", "#A1887F", "#8D6E63", "#795548", "#6D4C41", "#4E342E"],
    "Roxo": ["#E1BEE7", "#CE93D8", "#BA68C8", "#AB47BC", "#9C27B0", "#7B1FA2", "#4A148C"],
    "Preto": ["#9E9E9E", "#757575", "#616161", "#424242", "#212121", "#000000"],
    "Branco": ["#FFFFFF", "#FAFAFA", "#F5F5F5", "#EEEEEE", "#E0E0E0"]
}

# Estado para guardar as cores escolhidas
if 'cores_selecionadas' not in st.session_state:
    st.session_state.cores_selecionadas = []

# Selecionar cor base
cor_base_escolhida = st.selectbox("Escolha a cor base para ver os tons:", list(cores_base.keys()))

# Mostrar tons da cor base escolhida para seleção múltipla
tons_da_cor = cores_base[cor_base_escolhida]
tons_selecionados = st.multiselect(
    "Selecione um ou mais tons desta cor para sua paleta:",
    options=tons_da_cor,
    default=[cor for cor in tons_da_cor if cor in st.session_state.cores_selecionadas]
)

# Atualizar a lista global das cores escolhidas
# Adicionar os novos tons selecionados (sem duplicar)
for cor in tons_selecionados:
    if cor not in st.session_state.cores_selecionadas:
        st.session_state.cores_selecionadas.append(cor)
# Remover cores que não estão mais selecionadas nessa cor base
cores_nao_mais_selecionadas = [cor for cor in tons_da_cor if cor not in tons_selecionados and cor in st.session_state.cores_selecionadas]
for cor in cores_nao_mais_selecionadas:
    st.session_state.cores_selecionadas.remove(cor)

# Mostrar paleta final escolhida
st.write("### Paleta escolhida até agora:")
if st.session_state.cores_selecionadas:
    cols = st.columns(len(st.session_state.cores_selecionadas))
    for i, cor in enumerate(st.session_state.cores_selecionadas):
        with cols[i]:
            st.markdown(f'<div style="width: 100%; height: 60px; background-color: {cor}; border: 1px solid #000;"></div>', unsafe_allow_html=True)
            st.caption(cor)
else:
    st.write("Nenhuma cor escolhida ainda.")

# ---- OPÇÃO PERSONALIZADA ----
personalizada = st.checkbox("Quero sugerir uma paleta personalizada (descreva abaixo)")
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
        "Cores escolhidas": ", ".join(st.session_state.cores_selecionadas) if st.session_state.cores_selecionadas else "Nenhuma",
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
