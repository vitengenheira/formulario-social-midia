import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from io import BytesIO

# ---- CONFIGURAÇÃO DA PÁGINA ----
st.set_page_config(page_title="Formulário Social Mídia", layout="centered")

st.title("📱 Formulário de Início - Social Mídia")
st.write("Preencha os dados abaixo para começarmos a criar conteúdos incríveis para suas redes!")

# ---- COLETA DE DADOS BÁSICOS ----
nome = st.text_input("Nome completo")
profissao = st.text_input("Profissão")

# ---- LOGO ----
logo = st.radio("Você já tem uma logo?", ["Sim", "Não"])
logo_img = None
detalhes_logo = ""
if logo == "Sim":
    logo_img = st.file_uploader("Faça upload da sua logo (PNG/JPG)", type=["png", "jpg", "jpeg"])
else:
    detalhes_logo = st.text_area("Como você gostaria da sua logo? (Iniciais, ícone, desenho...)")

# ---- PALETA DE CORES ----
tem_paleta = st.radio("Você já tem uma paleta de cores?", ["Sim", "Não"])

paleta_cliente = ""
paleta_escolhida = []
if tem_paleta == "Sim":
    paleta_cliente = st.text_input("Qual a sua paleta? (Digite os códigos HEX separados por vírgula ou nomes)")
else:
    st.write("## Escolha sua paleta de cores")

    # Cores principais para escolher tons
    cores_principais = {
        "Vermelho": ["#FFEBEE", "#EF9A9A", "#E53935", "#B71C1C"],
        "Verde": ["#E8F5E9", "#A5D6A7", "#43A047", "#1B5E20"],
        "Azul": ["#E3F2FD", "#90CAF9", "#1E88E5", "#0D47A1"],
        "Amarelo": ["#FFFDE7", "#FFF59D", "#FDD835", "#F9A825"],
        "Roxo": ["#F3E5F5", "#CE93D8", "#8E24AA", "#4A148C"],
        "Marrom": ["#EFEBE9", "#BCAAA4", "#6D4C41", "#3E2723"],
        "Cinza": ["#FAFAFA", "#BDBDBD", "#616161", "#212121"],
        "Preto": ["#000000", "#212121", "#424242", "#616161"],
        "Branco": ["#FFFFFF", "#F5F5F5", "#EEEEEE", "#E0E0E0"],
    }

    # Seleção da cor principal
    cor_principal = st.selectbox("Escolha a cor principal:", list(cores_principais.keys()))

    # Mostrar tons para escolher (checkbox múltipla)
    tons = cores_principais[cor_principal]
    st.write("### Escolha um ou mais tons:")
    tons_selecionados = []
    cols = st.columns(len(tons))
    for i, cor in enumerate(tons):
        with cols[i]:
            selecionado = st.checkbox("", key=f"ton_{cor}", value=False)
            st.markdown(f'<div style="width: 50px; height: 50px; background-color: {cor}; border: 1px solid #000; margin: auto;"></div>', unsafe_allow_html=True)
            if selecionado:
                tons_selecionados.append(cor)

    # Combinação de paletas: o cliente pode adicionar outra cor
    adicionar_mais = st.checkbox("Adicionar outra cor principal para combinar?")
    if adicionar_mais:
        cor2 = st.selectbox("Escolha a segunda cor principal:", [c for c in cores_principais.keys() if c != cor_principal])
        tons2 = cores_principais[cor2]
        st.write("### Escolha tons adicionais:")
        tons_selecionados2 = []
        cols2 = st.columns(len(tons2))
        for i, cor in enumerate(tons2):
            with cols2[i]:
                selecionado = st.checkbox("", key=f"ton2_{cor}", value=False)
                st.markdown(f'<div style="width: 50px; height: 50px; background-color: {cor}; border: 1px solid #000; margin: auto;"></div>', unsafe_allow_html=True)
                if selecionado:
                    tons_selecionados2.append(cor)
        paleta_escolhida = tons_selecionados + tons_selecionados2
    else:
        paleta_escolhida = tons_selecionados

    if len(paleta_escolhida) == 0:
        st.warning("Escolha pelo menos um tom para continuar")

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
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2 ,4))

class PDF(FPDF):
    def color_box(self, x, y, w, h, color_hex):
        r, g, b = hex_to_rgb(color_hex)
        self.set_fill_color(r, g, b)
        self.rect(x, y, w, h, 'F')

def gerar_pdf(dados, nome_arquivo, logo_file):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Informações do Cliente - Social Mídia", ln=True, align="C")
    pdf.ln(10)

    # Logo
    if logo_file:
        # Como o arquivo vem do upload, precisamos salvar temporariamente ou usar BytesIO
        pdf.image(logo_file, x=10, y=20, w=40)
        pdf.ln(45)
    else:
        pdf.ln(10)

    pdf.set_font("Arial", 'B', 12)
    for chave, valor in dados.items():
        if chave == "Cores da paleta" and valor:
            pdf.cell(0, 10, f"{chave}:", ln=True)
            # Mostrar quadradinhos coloridos das cores
            x_start = pdf.get_x()
            y_start = pdf.get_y()
            box_size = 10
            espacamento = 5
            for i, cor in enumerate(valor):
                pdf.color_box(x_start + i*(box_size + espacamento), y_start, box_size, box_size, cor)
            pdf.ln(box_size + 8)
        else:
            pdf.set_font("Arial", '', 12)
            pdf.multi_cell(0, 8, f"{chave}: {valor}")
            pdf.ln(1)
    pdf.output(nome_arquivo)

# ---- ENVIO DO FORMULÁRIO ----
if st.button("Enviar formulário"):
    if nome.strip() == "" or profissao.strip() == "":
        st.error("Por favor, preencha nome e profissão.")
    elif tem_paleta == "Não" and len(paleta_escolhida) == 0:
        st.error("Escolha pelo menos um tom de cor na paleta.")
    else:
        data = datetime.now().strftime("%Y-%m-%d_%H-%M")
        nome_pdf = f"{nome.replace(' ', '')}{data}.pdf"

        cores_para_pdf = []
        if tem_paleta == "Sim":
            cores_para_pdf = [c.strip() for c in paleta_cliente.split(",") if c.strip()]
        else:
            cores_para_pdf = paleta_escolhida

        dados = {
            "Nome": nome,
            "Profissão": profissao,
            "Tem logo": logo,
            "Detalhes da logo": detalhes_logo if logo == "Não" else "Logo enviada",
            "Paleta própria?": tem_paleta,
            "Cores da paleta": cores_para_pdf,
            "Feed": "Sim" if feed else "Não",
            "Stories": "Sim" if story else "Não",
            "Reels": "Sim" if reels else "Não",
            "Roteiro Reels": roteiro,
            "Recorrência": recorrencia
        }

        # Preparar logo para PDF
        logo_path = None
        if logo_img is not None:
            logo_bytes = logo_img.getvalue()
            logo_path = f"temp_logo_{data}.png"
            with open(logo_path, "wb") as f:
                f.write(logo_bytes)

        gerar_pdf(dados, nome_pdf, logo_path)

        # Apagar arquivo temporário depois do PDF? (Opcional)

        st.success("✅ Formulário enviado e PDF gerado com sucesso!")
        st.download_button("📄 Baixar PDF agora", data=open(nome_pdf, "rb").read(), file_name=nome_pdf, mime="application/pdf")
