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

# ---- PALETA DE CORES ----
tem_paleta = st.radio("Você já tem uma paleta de cores definida?", ["Sim", "Não"])

paleta_existente = ""
cores_selecionadas = []

if tem_paleta == "Sim":
    paleta_existente = st.text_area("Por favor, descreva sua paleta de cores ou cole os códigos HEX aqui:")
else:
    st.write("## Escolha sua paleta de cores")

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

    if 'cores_selecionadas' not in st.session_state:
        st.session_state.cores_selecionadas = []

    for cor_base, tons in cores_base.items():
        with st.expander(f"{cor_base}"):
            tons_selecionados = st.multiselect(
                f"Selecione os tons de {cor_base} para sua paleta:",
                options=tons,
                default=[cor for cor in tons if cor in st.session_state.cores_selecionadas],
                key=f"tons_{cor_base}"
            )
            # Atualiza cores_selecionadas com tons escolhidos
            for cor in tons_selecionados:
                if cor not in st.session_state.cores_selecionadas:
                    st.session_state.cores_selecionadas.append(cor)
            # Remove tons que foram desmarcados
            tons_remover = [cor for cor in tons if cor not in tons_selecionados and cor in st.session_state.cores_selecionadas]
            for cor in tons_remover:
                st.session_state.cores_selecionadas.remove(cor)

    st.write("### Paleta escolhida até agora:")
    if st.session_state.cores_selecionadas:
        cols = st.columns(len(st.session_state.cores_selecionadas))
        for i, cor in enumerate(st.session_state.cores_selecionadas):
            with cols[i]:
                st.markdown(f'<div style="width: 100%; height: 60px; background-color: {cor}; border: 1px solid #000;"></div>', unsafe_allow_html=True)
                st.caption(cor)
    else:
        st.write("Nenhuma cor escolhida ainda.")

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

    if tem_paleta == "Sim":
        paleta_final = paleta_existente
    else:
        paleta_final = ", ".join(st.session_state.cores_selecionadas) if st.session_state.cores_selecionadas else "Nenhuma cor escolhida"

    dados = {
        "Nome": nome,
        "Profissão": profissao,
        "Tem logo": logo,
        "Detalhes da logo": detalhes_logo,
        "Tem paleta de cores?": tem_paleta,
        "Paleta escolhida": paleta_final,
        "Feed": "Sim" if feed else "Não",
        "Stories": "Sim" if story else "Não",
        "Reels": "Sim" if reels else "Não",
        "Roteiro Reels": roteiro,
        "Recorrência": recorrencia
    }

    gerar_pdf(dados, nome_pdf)
    st.success("✅ Formulário enviado e PDF gerado com sucesso!")
    st.download_button("📄 Baixar PDF agora", data=open(nome_pdf, "rb").read(), file_name=nome_pdf, mime="application/pdf")
