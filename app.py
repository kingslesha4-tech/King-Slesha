import streamlit as st
import datetime
import random
import pandas as pd
import time

PAYPAL_OFICIAL = "Kingslesha4@gmail.com"
SENHA_KING = "chila1990"

if "musicas" not in st.session_state:
    st.session_state["musicas"] = []
if "logado" not in st.session_state:
    st.session_state["logado"] = False

st.set_page_config(page_title="King Slesha Moz", page_icon="KING")
st.markdown("<h1 style='background:black;color:gold;text-align:center;padding:20px;border-radius:10px;'>KING SLESHA MOZ - DISTRIBUIDORA</h1>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Menu", ["Enviar Musica", "Painel King"])

if menu == "Enviar Musica":
    st.subheader("Enviar Musica")
    nome = st.text_input("Nome Artista *")
    email_a = st.text_input("Email Artista *")
    titulo = st.text_input("Titulo Musica *")
    genero = st.selectbox("Genero", ["Amapiano", "Afrobeat", "Hip Hop", "Marrabenta", "Pandza", "Outro"])

    st.write("---")
    st.subheader("Forma de Receber 70%")
    forma_pag = st.selectbox("Escolhe como quer receber", ["PayPal", "M-Pesa", "e-Mola", "Conta Bancaria"])

    paypal_a = ""
    mpesa_num = ""
    emola_num = ""
    banco_nome = ""
    banco_conta = ""
    banco_nib = ""

    if forma_pag == "PayPal":
        paypal_a = st.text_input("Seu PayPal 70% *", placeholder="seu@gmail.com")
    if forma_pag == "M-Pesa":
        mpesa_num = st.text_input("Seu Numero M-Pesa *", placeholder="84xxxxxxx")
    if forma_pag == "e-Mola":
        emola_num = st.text_input("Seu Numero e-Mola *", placeholder="82xxxxxxx")
    if forma_pag == "Conta Bancaria":
        banco_nome = st.selectbox("Banco", ["BCI", "Millennium BIM", "Standard Bank", "Moza Banco", "ABSA", "Outro"])
        banco_conta = st.text_input("Numero da Conta *")
        banco_nib = st.text_input("NIB *", placeholder="0000...")

    st.write("---")
    mp3 = st.file_uploader("MP3/WAV/M4A *", type=["mp3","wav","m4a"])
    capa = st.file_uploader("Capa 3000x3000 *", type=["jpg","png","jpeg"])
    ok = st.checkbox("Aceito contrato 70/30")

    # BOTAO COM TRAÇO DE PROGRESSO QUE TU MARCOU NA FOTO
    if st.button("ENVIAR PARA KING", use_container_width=True, type="primary"):
        if not ok or not nome or not titulo or not mp3:
            st.error("Preenche tudo!")
        else:
            # AQUI COMEÇA O TRAÇO QUE TU QUERES
            st.write("---")
            progresso_texto = st.empty()
            barra = st.progress(0)

            progresso_texto.write("Iniciando envio 0%")
            barra.progress(10)
            time.sleep(0.5)

            progresso_texto.write("Salvando MP3 " + mp3.name + " 30%")
            barra.progress(30)
            time.sleep(0.5)

            progresso_texto.write("Salvando capa 60%")
            barra.progress(60)
            time.sleep(0.5)

            progresso_texto.write("Gerando ISRC e enviando para distribuidora 85%")
            barra.progress(85)
            time.sleep(0.5)

            # SALVA DE VERDADE
            isrc = "MZ-KSM-25-" + str(random.randint(10000,99999))
            mp3_data = mp3.getvalue()
            capa_data = capa.getvalue() if capa else None

            nova = {
                "Data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Artista": nome,
                "Musica": titulo,
                "Genero": genero,
                "Email": email_a,
                "Forma Pag": forma_pag,
                "PayPal Artista": paypal_a,
                "M-Pesa": mpesa_num,
                "e-Mola": emola_num,
                "Banco": banco_nome,
                "Conta": banco_conta,
                "NIB": banco_nib,
                "ISRC": isrc,
                "Status": "Pendente",
                "mp3_bytes": mp3_data,
                "mp3_nome": mp3.name,
                "capa_bytes": capa_data,
                "capa_nome": capa.name if capa else None
            }
            st.session_state["musicas"].append(nova)

            barra.progress(100)
            progresso_texto.write("Concluido 100%")
            time.sleep(0.5)

            st.success("Recebido com sucesso! ISRC " + isrc + " - Musica terminou de enviar!")
            st.balloons()

else:
    st.subheader("Painel King Slesha")
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
        col1, col2, col3 = st.columns(3)
        total = len(st.session_state["musicas"])
        pendentes = 0
        for m in st.session_state["musicas"]:
            if m["Status"] == "P
