import streamlit as st
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime, random

# CONFIG KING ATUALIZADA
PAYPAL_OFICIAL = "Kingslesha4@gmail.com"
SENHA_KING = "Chila1990"
SEU_WHATSAPP = "258853772668"
SEU_EMAIL = "Kingslesha4@gmail.com"

def enviar_email(nome, titulo, email_art, paypal_art, isrc):
    try:
        msg = MIMEMultipart()
        msg['From'] = SEU_EMAIL
        msg['To'] = SEU_EMAIL
        msg['Subject'] = f"🎵 NOVA MUSICA: {titulo} - {nome}"
        corpo = f"""
👑 KING SLESHA MOZ - NOVA MUSICA RECEBIDA!

Artista: {nome}
Musica: {titulo}
Email Artista: {email_art}
PayPal 70%: {paypal_art}
ISRC Gerado: {isrc}
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}

Painel King: https://zpjg.streamlit.app
Senha: {SENHA_KING}
PayPal Oficial: {PAYPAL_OFICIAL}
WhatsApp King: +{SEU_WHATSAPP}
"""
        msg.attach(MIMEText(corpo, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SEU_EMAIL, st.secrets["EMAIL_PASSWORD"])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.write(f"Erro email: {e}")
        return False

def enviar_whatsapp(nome, titulo, email_art, paypal_art, isrc):
    try:
        apikey = st.secrets["CALLMEBOT_APIKEY"]
        mensagem = f"👑 KING! Nova musica recebida! 🎵 {titulo} 👤 {nome} 📧 {email_art} 💰 PayPal 70%: {paypal_art} 🆔 {isrc} Entra: zpjg.streamlit.app Senha: Chila1990"
        url = f"https://api.callmebot.com/whatsapp.php?phone={SEU_WHATSAPP}&text={requests.utils.quote(mensagem)}&apikey={apikey}"
        requests.get(url, timeout=15)
        return True
    except:
        return False

st.set_page_config(page_title="King Slesha Moz", page_icon="👑")
st.markdown(f"<h1 style='background:black;color:gold;text-align:center;padding:20px;border-radius:10px;'>👑 KING SLESHA MOZ</h1><p style='text-align:center;'>📧 {SEU_EMAIL} | 📱 +{SEU_WHATSAPP} | PayPal Oficial: {PAYPAL_OFICIAL}</p>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Menu", ["Enviar Musica", "Painel King"])

if menu == "Enviar Musica":
    with st.form("envio"):
        nome = st.text_input("Nome Artista *")
        email_a = st.text_input("Email Artista *")
        paypal_a = st.text_input("PayPal Artista 70% *")
        titulo = st.text_input("Título *", "Lefty Raite")
        mp3 = st.file_uploader("MP3/WAV *", type=["mp3","wav"])
        capa = st.file_uploader("Capa 3000x3000 *", type=["jpg","png"])
        ok = st.checkbox(f"Aceito 70/30 - PayPal {PAYPAL_OFICIAL} *")
        btn = st.form_submit_button("🚀 ENVIAR PARA KING", use_container_width=True, type="primary")
        
        if btn:
            if not ok or not nome or not titulo:
                st.error("Preenche tudo e marca contrato!")
            else:
                isrc = f"MZ-KSM-25-{random.randint(10000,99999)}"
                # SALVAR NO SUPABASE AQUI
                email_ok = enviar_email(nome, titulo, email_a, paypal_a, isrc)
                zap_ok = enviar_whatsapp(nome, titulo, email_a, paypal_a, isrc)
                
                st.success(f"✅ ISRC: {isrc}
