import streamlit as st
import datetime, random
import pandas as pd

PAYPAL_OFICIAL = "Kingslesha4@gmail.com"
SENHA_KING = "chila1990"

# Guarda musicas na memória
if "musicas" not in st.session_state:
    st.session_state["musicas"] = []

st.set_page_config(page_title="King Slesha Moz", page_icon="👑")
st.markdown("<h1 style='background:black;color:gold;text-align:center;padding:20px;border-radius:10px;'>KING SLESHA MOZ</h1>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Menu", ["Enviar Musica", "Painel King"])

if menu == "Enviar Musica":
    with st.form("envio"):
        nome = st.text_input("Nome Artista *")
        email_a = st.text_input("Email Artista *")
        paypal_a = st.text_input("PayPal Artista 70% *")
        titulo = st.text_input("Titulo Musica *")
        genero = st.selectbox("Genero", ["Amapiano", "Afrobeat", "Hip Hop", "Marrabenta", "Pandza", "Outro"])
        mp3 = st.file_uploader("MP3/WAV *", type=["mp3","wav"])
        capa = st.file_uploader("Capa 3000x3000 *", type=["jpg","png"])
        ok = st.checkbox(f"Aceito contrato 70/30 - PayPal {PAYPAL_OFICIAL} *")
        btn = st.form_submit_button("ENVIAR PARA KING", use_container_width=True, type="primary")
        
        if btn:
            if not ok or not nome or not titulo:
                st.error("Preenche tudo e marca contrato!")
            else:
                isrc = f"MZ-KSM-25-{random.randint(10000,99999)}"
                nova = {
                    "Data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Artista": nome,
                    "Musica": titulo,
                    "Genero": genero,
                    "Email": email_a,
                    "PayPal Artista": paypal_a,
                    "ISRC": isrc,
                    "Status": "Pendente"
                }
                st.session_state["musicas"].append(nova)
                st.success(f"Recebido! ISRC: {isrc} - Vamos distribuir em 24h!")
                st.balloons()

else:
    st.subheader("Painel King Slesha")
    
    if "logado" not in st.session_state:
        st.session_state["logado"] = False
    
    if not st.session_state["logado"]:
        senha = st.text_input("Senha King", type="password", placeholder="Digite sua senha")
        if st.button("ENTRAR NO PAINEL", use_container_width=True, type="primary"):
            if senha.lower().strip() == SENHA_KING:
                st.session_state["logado"] = True
                st.rerun()
            else:
                st.error("Senha incorreta!")
    else:
        st.success("Bem-vindo King!")
        
        # TUAS COISAS DE VOLTA
        col1, col2, col3 = st.columns(3)
        total = len(st.session_state["musicas"])
        pendentes = len([m for m in st.session_state["musicas"] if m["Status"] == "Pendente"])
        col1.metric("Total Musicas", total)
        col2.metric("Pendentes", pendentes)
        col3.metric("Status", "Online")
        
        col4, col5 = st.columns(2)
        col4.metric("PayPal Oficial", PAYPAL_OFICIAL)
        col5.metric("Divisao", "70% Artista / 30% King")
        
        st.write("---")
        st.subheader("Musicas dos Clientes para Aprovar")
        
        if total == 0:
            st.info("Nenhuma musica enviada ainda. As musicas dos clientes vao aparecer aqui.")
        else:
            df = pd.DataFrame(st.session_state["musicas"])
            st.dataframe(df, use_container_width=True)
            
            # Botao para aprovar
            if st.button("APROVAR TODAS PENDENTES", type="primary"):
                for m in st.session_state["musicas"]:
                    m["Status"] = "Aprovada - Distribuida"
                st.success("Todas aprovadas!")
                st.rerun()

        if st.button("SAIR"):
            st.session_state["logado"] = False
            st.rerun()
