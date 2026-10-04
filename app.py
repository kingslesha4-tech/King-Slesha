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
st.markdown("<h1 style='background:black;color:gold;text-align:center;padding:20px;border-radius:10px;'>KING SLESHA MOZ</h1>", unsafe_allow_html=True)

def registar_user(nome, email, senha):
    for u in st.session_state["users"]:
        if u.get("email","").lower() == email.lower():
            return False
    novo = {"nome": nome, "email": email.lower(), "senha": senha, "data": datetime.datetime.now().strftime("%d/%m/%Y")}
    st.session_state["users"].append(novo)
    return True

def login_user(email, senha):
    em = email.lower()
    # King
    if em == EMAIL_KING.lower():
        if senha == SENHA_KING:
            st.session_state["is_king"] = True
            st.session_state["logado"] = True
            st.session_state["current_user"] = {"nome": "King Slesha", "email": email}
            return True
    # Artista
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
    st.subheader("Criar Conta")
    nome_r = st.text_input("Nome Completo *")
    email_r = st.text_input("Email *")
    senha_r = st.text_input("Senha *", type="password")
    senha_r2 = st.text_input("Confirmar Senha *", type="password")
    if st.button("CRIAR CONTA", type="primary", use_container_width=True):
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
    if st.button("Entrar com Google"):
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
    st.info("King: kingslesha4@gmail.com / chila1990")

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
        paypal_a = st.text_input("Seu PayPal *")
    if forma_pag == "M-Pesa":
        mpesa_num = st.text_input("Seu M-Pesa *")
    if forma_pag == "e-Mola":
        emola_num = st.text_input("Seu e-Mola *")
    if forma_pag == "Conta Bancaria":
        banco_nome = st.selectbox("Banco", ["BCI", "BIM", "Standard Bank", "Moza", "ABSA", "Outro"])
        banco_conta = st.text_input("Numero Conta *")
        banco_nib = st.text_input("NIB *")
    mp3 = st
