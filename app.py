import streamlit as st
import requests
import datetime, random

PAYPAL_OFICIAL = "Kingslesha4@gmail.com"
SENHA_KING = "Chila1990"
SEU_WHATSAPP = "258853772668"

def enviar_whatsapp(nome, titulo, email_art, paypal_art, isrc):
    try:
        apikey = st.secrets["CALLMEBOT_APIKEY"]
        mensagem = f"""👑 KING SLESHA MOZ - NOVA MUSICA!

🎵 Titulo: {titulo}
👤 Artista: {nome}
📧 Email: {email_art}
💰 PayPal 70%: {paypal_art}
🆔 ISRC: {isrc}
📅 Data: {datetime.datetime.now().strftime('%d/%m %H:%M')}

Entra pra aprovar:
zpjg.streamlit.app
Senha: Chila1990
PayPal: {PAYPAL_OFICIAL}
"""
        url = f"https://api.callmebot.com/whatsapp.php?phone={SEU_WHATSAPP}&text={requests.utils.quote(mensagem)}&apikey={apikey}"
        r = requests.get(url, timeout=15)
        return True
    except Exception as e:
        st.error(f"Erro Zap: {e}")
        return False

st.set_page_config(page_title="King Slesha Moz", page_icon="👑")
st.markdown("<h1 style='background:black;color:gold;text-align:center;padding:20px;border-radius:10px;'>👑 KING SLESHA MOZ</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'>PayPal Oficial: {PAYPAL_OFICIAL} | WhatsApp: +{SEU_WHATSAPP}</p>", unsafe_allow_html=True)

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
        btn = st.form_submit_button("🚀 ENVIAR", use_container_width=True, type="primary")

        if btn:
            if not ok or not nome:
                st.error("Preenche tudo e aceita contrato!")
            else:
                isrc = f"MZ-KSM-25-{random.randint(10000,99999)}"
                # SALVA NO SUPABASE AQUI
                
                if enviar_whatsapp(nome, titulo, email_a, paypal_a, isrc):
                    st.success(f"✅ Enviado! ISRC: {isrc}")
                    st.success(f"📱 WhatsApp enviado pra +{SEU_WHATSAPP} - Olha teu WhatsApp!")
                    st.balloons()
                else:
                    st.warning("Salvo mas Zap falhou - verifica APIKEY nos Secrets")

else:
    st.subheader("👑 Painel King")
    senha = st.text_input("Senha King", type="password")
    if st.button("🔐 ENTRAR", use_container_width=True, type="primary"):
        if senha == SENHA_KING:
            st.session_state["logado"] = True
            st.success("Bem-vindo King!")
        else:
            st.error("Senha errada! É Chila1990")
    
    if st.session_state.get("logado"):
        st.metric("WhatsApp King", f"+{SEU_WHATSAPP}")
        if st.button("🚪 SAIR"):
           
