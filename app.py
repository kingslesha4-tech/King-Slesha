import streamlit as st
import requests
import datetime, random

PAYPAL_OFICIAL = "Kingslesha4@gmail.com"
SENHA_KING = "Chila1990"
SEU_WHATSAPP = "258853772668"
SEU_EMAIL = "Kingslesha4@gmail.com"

def enviar_whatsapp(nome, titulo, email_art, paypal_art, isrc):
    try:
        apikey = st.secrets["CALLMEBOT_APIKEY"]
        texto = f"KING SLESHA - Nova musica! Titulo: {titulo} - Artista: {nome} - Email: {email_art} - PayPal: {paypal_art} - ISRC: {isrc} - Painel: zpjg.streamlit.app Senha: Chila1990"
        url = f"https://api.callmebot.com/whatsapp.php?phone={SEU_WHATSAPP}&text={requests.utils.quote(texto)}&apikey={apikey}"
        requests.get(url, timeout=15)
        return True
    except:
        return False

def enviar_email(nome, titulo, email_art, paypal_art, isrc):
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        msg = MIMEMultipart()
        msg['From'] = SEU_EMAIL
        msg['To'] = SEU_EMAIL
        msg['Subject'] = f"Nova musica: {titulo} - {nome}"
        corpo = f"Artista: {nome}\nMusica: {titulo}\nEmail: {email_art}\nPayPal: {paypal_art}\nISRC: {isrc}\nData: {datetime.datetime.now()}\nPainel: https://zpjg.streamlit.app\nSenha: {SENHA_KING}"
        msg.attach(MIMEText(corpo, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SEU_EMAIL, st.secrets["EMAIL_PASSWORD"])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.write("Erro email:", e)
        return False

st.set_page_config(page_title="King Slesha Moz", page_icon="👑")
st.markdown("<h1 style='background:black;color:gold;text-align:center;padding:20px;border-radius:10px;'>KING SLESHA MOZ</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'>Email: {SEU_EMAIL} | WhatsApp: +{SEU_WHATSAPP}</p>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Menu", ["Enviar Musica", "Painel King"])

if menu == "Enviar Musica":
    with st.form("envio"):
        nome = st.text_input("Nome Artista *")
        email_a = st.text_input("Email Artista *")
        paypal_a = st.text_input("PayPal Artista 70% *")
        titulo = st.text_input("Titulo *", "Lefty Raite")
        mp3 = st.file_uploader("MP3/WAV *", type=["mp3","wav"])
        capa = st.file_uploader("Capa 3000x3000 *", type=["jpg","png"])
        ok = st.checkbox(f"Aceito 70/30 - PayPal {PAYPAL_OFICIAL} *")
        btn = st.form_submit_button("ENVIAR PARA KING", use_container_width=True, type="primary")
        
        if btn:
            if not ok or not nome or not titulo:
                st.error("Preenche tudo e marca contrato!")
            else:
                isrc = f"MZ-KSM-25-{random.randint(10000,99999)}"
                email_ok = enviar_email(nome, titulo, email_a, paypal_a, isrc)
                zap_ok = enviar_whatsapp(nome, titulo, email_a, paypal_a, isrc)
                
                st.success(f"Recebido! ISRC: {isrc}")
                if email_ok:
                    st.success(f"Email enviado para {SEU_EMAIL}")
                if zap_ok:
                    st.success(f"WhatsApp enviado para +{SEU_WHATSAPP}")
                st.balloons()

else:
    st.subheader("Painel King Slesha")
    senha = st.text_input("Senha King", type="password", placeholder="Chila1990")
    if st.button("ENTRAR NO PAINEL", use_container_width=True, type="primary"):
        if senha == SENHA_KING:
            st.session_state["logado"] = True
            st.success("Bem-vindo King!")
        else:
            st.error("Senha errada! Usa Chila1990")
    
    if st.session_state.get("logado"):
        col1, col2 = st.columns(2)
        col1.metric("Email King", SEU_EMAIL)
        col2.metric("WhatsApp King", f"+{SEU_WHATSAPP}")
        st.metric("PayPal Oficial", PAYPAL_OFICIAL)
        if st.button("SAIR"):
            st.session_state["logado"] = False
            st.rerun()
