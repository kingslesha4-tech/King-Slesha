import streamlit as st
import datetime, random

PAYPAL_OFICIAL = "Kingslesha4@gmail.com"
SENHA_KING = "Chila1990"

st.set_page_config(page_title="King Slesha Moz", page_icon="👑")
st.markdown("<h1 style='background:black;color:gold;text-align:center;padding:20px;border-radius:10px;'>KING SLESHA MOZ</h1>", unsafe_allow_html=True)

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
            if not ok or not nome:
                st.error("Preenche tudo!")
            else:
                isrc = f"MZ-KSM-25-{random.randint(10000,99999)}"
                st.success(f"Recebido! ISRC: {isrc}")
                st.balloons()

else:
    st.subheader("Painel King Slesha")
    
    # SENHA ANTIGA VOLTOU - ESCONDIDA
    if "logado" not in st.session_state:
        st.session_state["logado"] = False
    
    if not st.session_state["logado"]:
        senha = st.text_input("Senha King", type="password", placeholder="Digite sua senha")
        if st.button("ENTRAR NO PAINEL", use_container_width=True, type="primary"):
            if senha == SENHA_KING:
                st.session_state["logado"] = True
                st.rerun()
            else:
                st.error("Senha incorreta!")
    else:
        st.success("Bem-vindo King!")
        st.metric("PayPal Oficial", PAYPAL_OFICIAL)
        st.metric("Status", "Online")
        if st.button("SAIR"):
            st.session_state["logado"] = False
            st.rerun()
