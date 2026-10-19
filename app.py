import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="King Slesha Distribution", page_icon=":crown:", layout="wide")

DB_MUSICAS = "musicas_db.json"
DB_USERS = "users_db.json"
FOTOS_PASTA = "fotos_perfil"
os.makedirs(FOTOS_PASTA, exist_ok=True)

if not os.path.exists(DB_MUSICAS):
    with open(DB_MUSICAS, "w", encoding="utf-8") as f:
        json.dump([], f)
if not os.path.exists(DB_USERS):
    with open(DB_USERS, "w", encoding="utf-8") as f:
        json.dump([], f)

def load_musicas():
    try:
        with open(DB_MUSICAS, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_musicas(data):
    with open(DB_MUSICAS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_users():
    try:
        with open(DB_USERS, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_users(data):
    with open(DB_USERS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def salvar_foto(uploaded_file, email):
    if uploaded_file is None:
        return None
    ext = uploaded_file.name.split(".")[-1]
    nome = email.replace("@","_").replace(".","_") + "." + ext
    caminho = os.path.join(FOTOS_PASTA, nome)
    with open(caminho, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return caminho

ADMIN_PASSWORD = "King2026!"
ADMIN_EMAIL = "admin@kingslesha.com"

users_init = load_users()
tem_admin = False
for u in users_init:
    if u["email"] == ADMIN_EMAIL:
        tem_admin = True
if not tem_admin:
    users_init.append({
        "id": 1,
        "nome": "King Slesha ADMIN",
        "email": ADMIN_EMAIL,
        "senha": ADMIN_PASSWORD,
        "foto": None,
        "role": "admin",
        "criado": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "tipo_login": "email"
    })
    save_users(users_init)

if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

st.markdown("""
<style>
.king-header { text-align:center; padding:20px; background: linear-gradient(90deg,#FFD700,#FFA500); border-radius:15px; color:black; margin-bottom:20px; }
.stButton>button { background: #FFD700; color: black; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="king-header"><h1>KING-SLESHA MUSIC DISTRIBUTION</h1><p>De Matola para o Mundo</p></div>', unsafe_allow_html=True)

if st.session_state.usuario_logado is None:
    st.subheader("Plataforma King Slesha - Login")
    tab1, tab2 = st.tabs(["ENTRAR", "CRIAR CONTA"])

    with tab1:
        email_l = st.text_input("Email", key="login_email")
        senha_l = st.text_input("Senha",
