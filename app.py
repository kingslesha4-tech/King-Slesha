import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="King Slesha Distribution", page_icon="👑", layout="wide")

# ===== BANCO DE DADOS =====
DB_MUSICAS = "musicas_db.json"
DB_USERS = "users_db.json"
FOTOS_PASTA = "fotos_perfil"
os.makedirs(FOTOS_PASTA, exist_ok=True)

for arquivo in [DB_MUSICAS, DB_USERS]:
    if not os.path.exists(arquivo):
        with open(arquivo, "w") as f:
            json.dump([], f)

def load_musicas():
    try:
        with open(DB_MUSICAS, "r") as f:
            return json.load(f)
    except:
        return []

def save_musicas(data):
    with open(DB_MUSICAS, "w") as f:
        json.dump(data, f, indent=2)

def load_users():
    try:
        with open(DB_USERS, "r") as f:
            return json.load(f)
    except:
        return []

def save_users(data):
    with open(DB_USERS, "w") as f:
        json.dump(data, f, indent=2)

def salvar_foto(uploaded_file, email):
    if not uploaded_file:
        return None
    ext = uploaded_file.name.split('.')[-1]
    nome_arquivo = f"{email.replace('@','_').replace('.','_')}.{ext}"
    caminho = os.path.join(FOTOS_PASTA, nome_arquivo)
    with open(caminho, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return caminho

ADMIN_PASSWORD = "King2026!"
ADMIN_EMAIL = "admin@kingslesha.com"

# Cria admin automaticamente
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
    .foto-perfil { border-radius:50%; border:3px solid #FFD700; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="king-header"><h1>👑 KING-SLESHA MUSIC DISTRIBUTION</h1><p>De Matola para o Mundo 🌍</p></div>', unsafe_allow_html=True)

# ====== SE NÃO ESTÁ LOGADO -> LOGIN E REGISTRO ======
if st.session_state.usuario_logado is None:
    st.subheader("🔐 Plataforma King Slesha - Crie sua conta de Artista")
    
    tab_login, tab_registro = st.tabs(["🔑 ENTRAR", "👤 CRIAR CONTA COM GOOGLE OU EMAIL"])
    
    with tab_login:
        st.write("#### Entrar com Email")
        email_l = st.text_input("Email", key="l_email")
        senha_l = st.text_input("Senha", type="password", key="l_senha")
        if st.button("🚀 Entrar", use_container_width=True):
            users = load_users()
            achado = next((u for u in users if u['email'] == email_l and u['senha'] == senha_l), None)
            if achado:
                if not achado.get('foto'):
                    st.warning("⚠️ Você ainda não tem foto de perfil! Adicione no seu perfil após logar.")
                st.session_state.usuario_logado = achado
                st.success(f"Bem-vindo {achado['nome']}!")
                st.rerun()
            else:
                st.error("Email ou senha errados!")
        
        st.divider()
        st.write("#### 🔵 Entrar com Google (Simulação - depois conecta Firebase)")
        g_email_l = st.text_input("Seu Gmail", key="g_login_email")
        if st.button("🔵 Entrar com Google"):
            users = load_users()
            achado = next((u for u in users if u['email'] == g_email_l), None)
            if achado:
                st.session_state.usuario_logado = achado
                st.success("Login Google OK!")
                st.rerun()
            else:
                st.error("Conta Google não encontrada. Crie conta na aba Criar Conta!")

    with tab_registro:
        st.warning("📸 FOTO DE PERFIL É OBRIGATÓRIA PARA TODO ARTISTA!")
        
        col1, col2 = st.columns(2)
        with col1:
            nome_r = st.text_input("Nome Artístico *", key="r_nome")
            email_r = st.text_input("Email *", key="r_email")
        with col2:
            senha_r = st.text_input("Senha *", type="password", key="r_senha")
            senha_r2 = st.text_input("Confirmar Senha *", type="password", key="r_senha2")
        
        tipo_conta = st.radio("Tipo de conta:", ["📧 Email", "🔵 Google"], horizontal=True)
        
        foto_r = st.file_uploader("FOTO DE PERFIL * OBRIGATÓRIA (JPG/PNG)", type=["jpg","png","jpeg"], key="r_foto")
        if foto_r:
            st.image(foto_r, width=150, caption="Sua foto de perfil")
        
        if st.button("👑 CRIAR MINHA CONTA DE
