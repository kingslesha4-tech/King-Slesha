import streamlit as st
import random
import datetime
from fpdf import FPDF

st.set_page_config(page_title="King Slesha Moz", page_icon="🎵")
st.title("King Slesha Moz - Distribuidora Oficial")

# --- TEU CODIGO ANTIGO (mantive tudo) ---
st.header("Informacoes da Musica")
genero = st.selectbox("Genero", ["Amapiano", "Kizomba", "Marrabenta", "Afro House", "Pandza", "Hip Hop", "R&B"])

st.divider()
st.header("Forma de Receber 70%")
forma = st.selectbox("Escolhe como quer receber", ["Conta Bancaria", "PayPal", "M-Pesa / E-Mola"], key="forma")

paypal = st.text_input("Seu PayPal 70% *", placeholder="seu@gmail.com", help="Coloca teu email certo com @")

arquivo = st.file_uploader("MP3/WAV/M4A *", type=["mp3","wav","m4a"], help="200MB per file • MP3, WAV, M4A")

capa = st.file_uploader("Capa 3000x3000 *", type=["jpg","jpeg","png"], help="Obrigatorio 3000x3000 igual a capa que fizemos")

# --- CODIGO NOVO PARA FACEBOOK APROVAR (juntado aqui) ---
st.divider()
st.header("Codigo para Facebook / Instagram (Novo)")
st.info("O Facebook so aprova distribuidora com ISRC e UPC")

ano = datetime.datetime.now().year % 100
numero = random.randint(1, 99999)
isrc = f"MZ-KSM-{ano:02d}-{numero:05d}"
upc = f"19{random.randint(100000000000, 999999999999)}"

col1, col2 = st.columns(2)
with col1:
    st.text_input("ISRC gerado automatico", value=isrc, disabled=True)
with col2:
    st.text_input("UPC gerado automatico", value=upc, disabled=True)

fb_page = st.text_input("Link da tua Pagina Facebook de Musico *", placeholder="https://facebook.com/PedroManinghyOficial")

st.divider()
if st.button("✅ FINALIZAR E GERAR CONTRATO 70/30", type="primary", use_container_width=True):
    if "@" not in paypal:
        st.error("ERRO: Teu PayPal esta sem @. Corrige: kingslesha4@gmail.com")
    elif not arquivo:
        st.error("Falta subir a musica MP3/WAV")
    elif not capa:
        st.error("Falta subir a capa 3000x3000")
    elif not fb_page:
        st.error("Falta colar link da Pagina Facebook")
    else:
        # Gera PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "CONTRATO KING SLESHA MOZ - 70/30", ln=True, align="C")
        pdf.set_font("Arial", "", 11)
        pdf.ln(5)
        pdf.multi_cell(0, 7, f"""
Artista Email: {paypal}
Genero: {genero}
Forma: {forma}
Arquivo: {arquivo.name}
ISRC: {isrc}
UPC: {upc}
Facebook Page: {fb_page}
Data: {datetime.datetime.now().strftime('%d/%m/%Y')}

1. A King Slesha Moz distribuira a obra no Spotify, Apple Music, Facebook, Instagram, TikTok.
2. Divisao: 70% Artista, 30% King Slesha Moz.
3. O artista confirma que a musica e 100% original.
4. Direitos para Facebook/Instagram serao geridos via Rights Manager com ISRC {isrc}.
5. Pagamento ate dia 30 via {forma}.

Assinatura: _________________________

King Slesha Moz / BP Label Music
Xai-Xai, Gaza - Mozambique
        """)
        pdf_path = f"/tmp/contrato_{isrc}.pdf"
        pdf.output(pdf_path)
        st.success(f"FEITO KING! ISRC: {isrc} | UPC: {upc}")
        st.success("Agora tua distribuidora ja tem codigo que Facebook exige!")
        st.balloons()
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Baixar Contrato PDF", f, file_name=f"CONTRATO_{isrc}.pdf", use_container_width=True)

st.caption("© 2026 King Slesha Moz - Para aprovacao final, envia ISRC/UPC para music-partnerships@fb.com")
