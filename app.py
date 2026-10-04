import streamlit as st
import datetime
import random
import pandas as pd
import time

PAYPAL_OFICIAL = "Kingslesha4@gmail.com"
SENHA_KING = "chila1990"
EMAIL_KING = "kingslesha4@gmail.com"

if "musicas" not in st.session_state:
    st.session_state["musicas"] = []
if "pagamentos" not in st.session_state:
    st.session_state["pagamentos"] = []
if "users" not in st.session_state:
    st.session_state["users"] = []
if "logado" not in st.session_state:
    st.session_state["logado"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
if "is_king" not in st.session_state:
    st.session_state["is_king"] = False

st.set_page_config(page_title="King Slesha Moz", page_icon="KING")
st.markdown("<h1 style='background:black;color:gold;text-align:center;padding:20px;border-radius:10px;'>KING SLESHA MOZ - DISTRIBUIDORA</h1>", unsafe_allow_html=True)

def registar_user(nome, email, senha):
    for u in st.session_state["users"]:
        if u.get("email","").lower() == email.lower():
            return False
    novo = {"nome": nome, "email": email.lower(), "senha": senha, "data": datetime.datetime.now().strftime("%d/%m/%Y")}
    st.session_state["users"].append(novo)
    return True

def login_user(email, senha):
    em = email.lower()
    if em == EMAIL_KING.lower():
        if senha == SENHA_KING:
            st.session_state["is_king"] = True
            st.session_state["logado"] = True
            st.session_state["current_user"] = {"nome": "King Slesha", "email": email}
            return True
    for u in st.session_state["users"]:
        ue = u.get("email","").lower()
        us = u.get("senha","")
        if ue == em:
            if us == senha:
                st.session_state["current_user"] = u
                st.session_state["is_king"] = False
                st.session_state["logado"] = True
                return True
    return False

if not st.session_state["logado"]:
    menu = st.sidebar.selectbox("Menu", ["Login", "Registar", "Painel King"])
else:
    if st.session_state["is_king"]:
        menu = st.sidebar.selectbox("Menu King", ["Painel King", "Sair"])
    else:
        menu = st.sidebar.selectbox("Menu Artista", ["Enviar Musica", "Minhas Musicas", "Sair"])
        st.sidebar.success("Logado: " + st.session_state["current_user"].get("nome",""))

if menu == "Registar" and not st.session_state["logado"]:
    st.subheader("Criar Conta - Cada cliente cria sua conta")
    nome_r = st.text_input("Nome Completo *")
    email_r = st.text_input("Email *", placeholder="seu@gmail.com")
    senha_r = st.text_input("Senha *", type="password")
    senha_r2 = st.text_input("Confirmar Senha *", type="password")
    if st.button("CRIAR CONTA COM EMAIL", type="primary", use_container_width=True):
        if not nome_r or not email_r or not senha_r:
            st.error("Preenche tudo!")
        elif senha_r!= senha_r2:
            st.error("Senhas diferentes!")
        else:
            if registar_user(nome_r, email_r, senha_r):
                st.success("Conta criada! Faz Login!")
                st.balloons()
            else:
                st.error("Email ja existe!")
    st.write("---")
    email_g = st.text_input("Ou seu Gmail Google")
    if st.button("CONTINUAR COM GOOGLE", use_container_width=True):
        if email_g:
            registar_user(email_g.split("@")[0], email_g, "google123")
            login_user(email_g, "google123")
            st.rerun()

if menu == "Login" and not st.session_state["logado"]:
    st.subheader("Entrar")
    email_l = st.text_input("Email *")
    senha_l = st.text_input("Senha *", type="password")
    if st.button("ENTRAR", type="primary", use_container_width=True):
        if login_user(email_l, senha_l):
            st.rerun()
        else:
            st.error("Email ou senha errada!")

if menu == "Enviar Musica" and st.session_state["logado"] and not st.session_state["is_king"]:
    cur = st.session_state["current_user"]
    user_nome = cur.get("nome","")
    user_email = cur.get("email","")
    st.subheader("Enviar Musica - " + user_nome)
    nome = st.text_input("Nome Artista *", value=user_nome)
    email_a = st.text_input("Email Artista *", value=user_email)
    titulo = st.text_input("Titulo Musica *")
    genero = st.selectbox("Genero", ["Amapiano", "Afrobeat", "Hip Hop", "Marrabenta", "Pandza", "Kizomba", "Zouk", "Afro House", "R&B", "Outro"])
    forma_pag = st.selectbox("Forma de Receber 70%", ["PayPal", "M-Pesa", "e-Mola", "Conta Bancaria"])
    paypal_a = ""
    mpesa_num = ""
    emola_num = ""
    banco_nome = ""
    banco_conta = ""
    banco_nib = ""
    if forma_pag == "PayPal":
        paypal_a = st.text_input("Seu PayPal 70% *")
    if forma_pag == "M-Pesa":
        mpesa_num = st.text_input("Seu M-Pesa *")
    if forma_pag == "e-Mola":
        emola_num = st.text_input("Seu e-Mola *")
    if forma_pag == "Conta Bancaria":
        banco_nome = st.selectbox("Banco", ["BCI", "Millennium BIM", "Standard Bank", "Moza Banco", "ABSA", "Outro"])
        banco_conta = st.text_input("Numero Conta *")
        banco_nib = st.text_input("NIB *")
    mp3 = st.file_uploader("MP3/WAV/M4A *", type=["mp3","wav","m4a","mp4"])
    capa = st.file_uploader("Capa 3000x3000 *", type=["jpg","png","jpeg"])
    ok = st.checkbox("Aceito contrato 70/30")
    if st.button("ENVIAR PARA KING", use_container_width=True, type="primary"):
        if not ok or not nome or not titulo or not mp3:
            st.error("Preenche tudo!")
        else:
            texto = st.empty()
            barra = st.progress(0)
            texto.write("Iniciando envio 0%")
            barra.progress(10)
            time.sleep(0.3)
            texto.write("Salvando MP3 30%")
            barra.progress(30)
            time.sleep(0.3)
            texto.write("Salvando capa 60%")
            barra.progress(60)
            time.sleep(0.3)
            texto.write("Gerando ISRC 85%")
            barra.progress(85)
            time.sleep(0.3)
            isrc = "MZ-KSM-25-" + str(random.randint(10000,99999))
            mp3_data = mp3.getvalue()
            capa_data = capa.getvalue() if capa else None
            nova = {
                "Data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Artista": nome,
                "Musica": titulo,
                "Genero": genero,
                "Email": email_a,
                "Email Dono": user_email,
                "Forma Pag": forma_pag,
                "PayPal Artista": paypal_a,
                "M-Pesa": mpesa_num,
                "e-Mola": emola_num,
                "Banco": banco_nome,
                "Conta": banco_conta,
                "NIB": banco_nib,
                "ISRC": isrc,
                "Status": "Pendente",
                "Enviado Plataforma": "Nao",
                "Data Envio Plat": "",
                "Plataformas": "",
                "mp3_bytes": mp3_data,
                "mp3_nome": mp3.name,
                "capa_bytes": capa_data,
                "capa_nome": capa.name if capa else None
            }
            st.session_state["musicas"].append(nova)
            barra.progress(100)
            texto.write("Concluido 100% - Musica terminou!")
            st.success("Recebido! ISRC " + isrc)
            st.balloons()

if menu == "Minhas Musicas" and st.session_state["logado"] and not st.session_state["is_king"]:
    st.subheader("Minhas Musicas")
    user_email = st.session_state["current_user"].get("email","")
    minhas = []
    for m in st.session_state["musicas"]:
        if m.get("Email Dono","").lower() == user_email.lower() or m.get("Email","").lower() == user_email.lower():
            minhas.append(m)
    if len(minhas) == 0:
        st.info("Ainda nao enviaste musica")
    else:
        for m in minhas:
            tit = m.get("Musica","") + " - " + m.get("Status","")
            with st.expander(tit):
                st.write("Genero: " + m.get("Genero",""))
                if m.get("mp3_bytes"):
                    st.audio(m.get("mp3_bytes"), format="audio/mp3")
                    st.download_button("BAIXAR MUSICA", m.get("mp3_bytes"), file_name=m.get("mp3_nome","musica.mp3"), key="minha_mp3_" + m.get("ISRC",""))

# PAINEL KING - AGORA COM MUSICA PARA OUVIR E BAIXAR CORRIGIDO
if menu == "Painel King":
    st.subheader("Painel King Slesha")
    if not st.session_state["logado"] or not st.session_state["is_king"]:
        email_k = st.text_input("Email King", value="kingslesha4@gmail.com")
        senha_k = st.text_input
