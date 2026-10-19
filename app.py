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
    if u.get("email") == ADMIN_EMAIL:
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

st.markdown('<div style="text-align:center; padding:20px; background: linear-gradient(90deg,#FFD700,#FFA500); border-radius:15px; color:black;"><h1>KING-SLESHA MUSIC DISTRIBUTION</h1><p>De Matola para o Mundo</p></div>', unsafe_allow_html=True)

if st.session_state.usuario_logado is None:
    st.subheader("Plataforma King Slesha - Login")
    tab1, tab2 = st.tabs(["ENTRAR", "CRIAR CONTA"])

    with tab1:
        email_l = st.text_input("Email", key="login_email")
        senha_l = st.text_input("Senha", type="password", key="login_senha")
        if st.button("Entrar", use_container_width=True, key="btn_entrar"):
            users = load_users()
            achado = None
            for u in users:
                if u.get("email") == email_l and u.get("senha") == senha_l:
                    achado = u
            if achado:
                st.session_state.usuario_logado = achado
                st.rerun()
            else:
                st.error("Email ou senha errados")
        st.divider()
        g_email = st.text_input("Seu Gmail", key="g_login")
        if st.button("Entrar com Google", key="btn_glogin"):
            users = load_users()
            achado = None
            for u in users:
                if u.get("email") == g_email:
                    achado = u
            if achado:
                st.session_state.usuario_logado = achado
                st.rerun()
            else:
                st.error("Conta nao encontrada")

    with tab2:
        st.warning("FOTO DE PERFIL OBRIGATORIA!")
        nome_r = st.text_input("Nome Artistico", key="reg_nome")
        email_r = st.text_input("Email", key="reg_email")
        senha_r = st.text_input("Senha", type="password", key="reg_senha")
        senha_r2 = st.text_input("Confirmar Senha", type="password", key="reg_senha2")
        tipo_conta = st.radio("Tipo", ["Email", "Google"], horizontal=True, key="tipo")
        foto_r = st.file_uploader("Foto de perfil obrigatoria", type=["jpg","png","jpeg"], key="reg_foto")
        if foto_r is not None:
            st.image(foto_r, width=120)
        if st.button("CRIAR CONTA DE ARTISTA", use_container_width=True, key="btn_criar"):
            if not nome_r or not email_r or not senha_r:
                st.error("Preencha tudo")
            elif senha_r != senha_r2:
                st.error("Senhas diferentes")
            elif foto_r is None:
                st.error("Foto obrigatoria!")
            else:
                users = load_users()
                existe = False
                for u in users:
                    if u.get("email") == email_r:
                        existe = True
                if existe:
                    st.error("Email ja existe")
                else:
                    caminho = salvar_foto(foto_r, email_r)
                    novo = {
                        "id": len(users)+1,
                        "nome": nome_r,
                        "email": email_r,
                        "senha": senha_r,
                        "foto": caminho,
                        "role": "artist",
                        "criado": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "tipo_login": "google" if tipo_conta == "Google" else "email"
                    }
                    users.append(novo)
                    save_users(users)
                    st.session_state.usuario_logado = novo
                    st.balloons()
                    st.rerun()
    st.stop()

usuario = st.session_state.usuario_logado

with st.sidebar:
    st.write("Meu Perfil")
    if usuario.get("foto") and os.path.exists(usuario["foto"]):
        st.image(usuario["foto"], width=150)
    st.write(usuario.get("nome",""))
    st.write(usuario.get("email",""))
    st.write(usuario.get("role",""))
    nova_foto = st.file_uploader("Trocar foto", type=["jpg","png","jpeg"], key="troca")
    if nova_foto is not None:
        if st.button("Salvar foto", key="btn_foto"):
            caminho = salvar_foto(nova_foto, usuario.get("email",""))
            users = load_users()
            for u in users:
                if u.get("id") == usuario.get("id"):
                    u["foto"] = caminho
            save_users(users)
            st.session_state.usuario_logado["foto"] = caminho
            st.rerun()
    if st.button("Sair", key="btn_sair"):
        st.session_state.usuario_logado = None
        st.rerun()
    st.divider()
    if usuario.get("role") == "admin":
        menu = st.radio("MENU", ["Enviar Musica", "APROVACAO ADMIN", "Musicas no Ar", "TODAS CONTAS ARTISTAS"], key="menu_admin")
    else:
        menu = st.radio("MENU", ["Enviar Musica", "Musicas no Ar"], key="menu_art")

if menu == "Enviar Musica":
    st.subheader("Enviar musica")
    nome_artista = st.text_input("Nome do Artista", value=usuario.get("nome",""))
    nome_musica = st.text_input("Nome da Musica")
    tipo = st.selectbox("Tipo", ["Single", "Album", "EP"])
    genero = st.selectbox("Genero", ["Amapiano", "Afrobeat", "Hip Hop", "R&B", "Kizomba", "Marrabenta", "Outro"])
    label = st.text_input("Label", value="King Slesha Music Distribution")
    plataformas = st.multiselect("Plataformas", ["Spotify", "Apple Music", "YouTube Music", "Deezer", "Boomplay", "TikTok", "Audiomack"], default=["Spotify", "Apple Music"])
    audio = st.file_uploader("Audio", type=["mp3","wav","m4a"])
    capa = st.file_uploader("Capa", type=["jpg","png","jpeg"])
    if st.button("Distribuir Agora", key="btn_enviar"):
        if not nome_artista or not nome_musica or not audio:
            st.error("Preencha tudo")
        else:
            musicas = load_musicas()
            nova = {
                "id": len(musicas)+1,
                "user_id": usuario.get("id"),
                "user_nome": usuario.get("nome"),
                "user_email": usuario.get("email"),
                "user_foto": usuario.get("foto"),
                "artista": nome_artista,
                "musica": nome_musica,
                "tipo": tipo,
                "genero": genero,
                "label": label,
                "plataformas": plataformas,
                "arquivo": audio.name,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "status": "PENDENTE"
            }
            musicas.append(nova)
            save_musicas(musicas)
            st.success("Enviada!")
            st.balloons()

elif menu == "APROVACAO ADMIN":
    st.subheader("APROVACAO")
    musicas = load_musicas()
    pendentes = [m for m in musicas if m.get("status") == "PENDENTE"]
    st.metric("Pendentes", len(pendentes))
    for m in pendentes:
        st.write(m.get("musica","") + " - " + m.get("artista",""))
        col1, col2 = st.columns(2)
        with col1:
            if st.button("APROVAR", key=f"ap_{m.get('id')}"):
                for x in musicas:
                    if x.get("id") == m.get("id"):
                        x["status"] = "APROVADO"
                save_musicas(musicas)
                st.rerun()
        with col2:
            if st.button("REJEITAR", key=f"rej_{m.get('id')}"):
                for x in musicas:
                    if x.get("id") == m.get("id"):
                        x["status"] = "REJEITADO"
                save_musicas(musicas)
                st.rerun()

elif menu == "TODAS CONTAS ARTISTAS":
    st.subheader("TODAS CONTAS - ADMIN VE TUDO")
    users = load_users()
    st.metric("Total", len(users))
    for u in users:
        c1, c2 = st.columns([1,3])
        with c1:
            f = u.get("foto")
            if f and os.path.exists(f):
                st.image(f, width=80)
        with c2:
            st.write(u.get("nome","") + " - " + u.get("email","") + " - " + u.get("tipo_login",""))
            st.write(u.get("criado",""))
    st.dataframe([{"ID":u.get("id"),"Nome":u.get("nome"),"Email":u.get("email"),"Foto":"SIM" if u.get("foto") else "NAO","Tipo":u.get("tipo_login")} for u in users], use_container_width=True)

else:
    st.subheader("Musicas Aprovadas")
    musicas = load_musicas()
    aprovadas = [m for m in musicas if m.get("status") == "APROVADO"]
    for m in aprovadas:
        st.write(m.get("musica","") + " - " + m.get("artista",""))

st.sidebar.write("King-Slesha 2026")
