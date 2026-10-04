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
        if u["email"].lower() == email.lower():
            return False
    st.session_state["users"].append({"nome": nome, "email": email.lower(), "senha": senha, "data": datetime.datetime.now().strftime("%d/%m/%Y")})
    return True

def login_user(email, senha):
    if email.lower() == EMAIL_KING.lower() and senha == SENHA_KING:
        st.session_state["is_king"] = True
        st.session_state["logado"] = True
        st.session_state["current_user"] = {"nome": "King Slesha", "email": email}
        return True
    for u in st.session_state["users"]:
        if u["email"].lower() == email.lower() and u["senha"]
