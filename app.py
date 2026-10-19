import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="King Slesha Distribution", page_icon=":crown:", layout="wide")

# BANCOS
DB_MUSICAS = "musicas_db.json"
DB_USERS = "users_db.json"
FOTOS_PASTA = "fotos_perfil"
os.makedirs(FOTOS_PASTA, exist_ok=True)

for arquivo in [DB_MUSICAS, DB_USERS]:
    if not os.path.exists(arquivo):
        with open(arquivo, "w", encoding="utf-8") as f:
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

def salvar_foto_perfil(uploaded_file, email):
    if not uploaded_file:
        return None
    ext = uploaded_file.name.split('.')[-1]
    nome = f"{email.replace('@','_').replace('.','_')}.{ext}"
    caminho = os.path.join(FOTOS_PASTA, nome)
    with open(caminho, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return caminho

ADMIN_PASSWORD = "King2026!"
ADMIN_EMAIL = "admin@kingslesha.com"

users_init = load_users()
if not any(u['email'] == ADMIN_EMAIL for u in users_init):
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

if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = None

st.markdown("""
<style>
    .king-header { text-align:center; padding:20px; background: linear-gradient(90deg,#FFD700,#FFA500); border-radius:15px; color:black; margin-bottom:20px; }
    .stButton>button { background: #FFD700; color: black; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="king-header"><h1>KING-SLESHA MUSIC DISTRIBUTION</h1><p>De Matola para o Mundo</p></div>', unsafe_allow_html=True)

# LOGIN
if st.session_state.usuario_logado is None:
    st.subheader("Entrar - Plataforma King Slesha")
    
    tab1, tab2 = st.tabs(["ENTRAR", "CRIAR CONTA"])
    
    with tab1:
        email_l = st.text_input("Email", key="login_email")
        senha_l = st.text_input("Senha", type="password", key="login_senha")
        if st.button("Entrar", use_container_width=True):
            users = load_users()
            user = next((u for u in users if u['email'] == email_l and u['senha'] == senha_l), None)
            if user:
                st.session_state.usuario_logado = user
                st.success(f"Bem-vindo {user['nome']}!")
                st.rerun()
            else:
                st.error("Email ou senha errados!")

        st.divider()
        st.write("Login com Google - Simulacao")
        g_email_l = st.text_input("Seu Gmail", key="g_login_email")
        if st.button("Entrar com Google"):
            users = load_users()
            achado = next((u for u in users if u['email'] == g_email_l), None)
            if achado:
                st.session_state.usuario_logado = achado
                st.success("Login Google OK!")
                st.rerun()
            else:
                st.error("Conta nao encontrada. Crie conta!")

    with tab2:
        st.warning("FOTO DE PERFIL E OBRIGATORIA!")
        nome_r = st.text_input("Nome Artistico *", key="reg_nome")
        email_r = st.text_input("Email *", key="reg_email")
        senha_r = st.text_input("Senha *", type="password", key="reg_senha")
        senha_r2 = st.text_input("Confirmar Senha *", type="password", key="reg_senha2")
        tipo_login = st.radio("Tipo de conta:", ["Email", "Google"], horizontal=True)
        foto_r = st.file_uploader("FOTO DE PERFIL * OBRIGATORIA", type=["jpg","png","jpeg"], key="reg_foto")
        if foto_r:
            st.image(foto_r, width=120, caption="Preview")
        
        # CORRECAO AQUI - SEM EMOJI NO BUTTON
        if st.button("CRIAR MINHA CONTA DE ARTISTA", use_container_width=True):
            if not nome_r or not email_r or not senha_r:
                st.error("Preencha tudo!")
            elif senha_r != senha_r2:
                st.error("Senhas nao coincidem!")
            elif not foto_r:
                st.error("FOTO OBRIGATORIA! Adicione foto!")
            else:
                users = load_users()
                if any(u['email'] == email_r for u in users):
                    st.error("Email ja existe!")
                else:
                    caminho = salvar_foto_perfil(foto_r, email_r)
                    novo = {
                        "id": len(users)+1,
                        "nome": nome_r,
                        "email": email_r,
                        "senha": senha_r,
                        "foto": caminho,
                        "role": "artist",
                        "criado": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "tipo_login": "google" if tipo_login == "Google" else "email"
                    }
                    users.append(novo)
                    save_users(users)
                    st.session_state.usuario_logado = novo
                    st.success("Conta criada!")
                    st.balloons()
                    st.rerun()
    
    st.stop()

usuario = st.session_state.usuario_logado

with st.sidebar:
    st.markdown("### Meu Perfil")
    if usuario.get('foto') and os.path.exists(usuario['foto']):
       
