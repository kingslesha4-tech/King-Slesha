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

def e_admin(email):
    lista_admin = ["admin@kingslesha.com", "kingslesha4@gmail.com", "kingslesha@gmail.com"]
    return email.lower() in [e.lower() for e in lista_admin]

ADMIN_PASSWORD = "King2026!"

# Cria e atualiza admins
users_init = load_users()
mudou = False
for u in users_init:
    if e_admin(u.get("email","")) and u.get("role") != "admin":
        u["role"] = "admin"
        mudou = True

# Cria admin principal se nao existe
tem_admin_principal = False
for u in users_init:
    if u.get("email") == "admin@kingslesha.com":
        tem_admin_principal = True

if not tem_admin_principal:
    users_init.append({
        "id": 1,
        "nome": "King Slesha ADMIN",
        "email": "admin@kingslesha.com",
        "senha": ADMIN_PASSWORD,
        "foto": None,
        "role": "admin",
        "criado": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "tipo_login": "email"
    })
    mudou = True

if mudou:
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
                # Promove para admin se for da lista
                if e_admin(achado.get("email","")):
                    achado["role"] = "admin"
                    for uu in users:
                        if uu.get("id") == achado.get("id"):
                            uu["role"] = "admin"
                    save_users(users)
                st.session_state.usuario_logado = achado
                st.rerun()
            else:
                st.error("Email ou senha errados")

        st.divider()
        st.write("Login com Google")
        g_email = st.text_input("Seu Gmail", key="g_login")
        if st.button("Entrar com Google", key="btn_glogin"):
            users = load_users()
            achado = None
            for u in users:
                if u.get("email") == g_email:
                    achado = u
            if achado:
                if e_admin(achado.get("email","")):
                    achado["role"] = "admin"
                st.session_state.usuario_logado = achado
                st.rerun()
            else:
                st.error("Conta nao encontrada. Crie conta.")

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
                    role_novo = "admin" if e_admin(email_r) else "artist"
                    novo = {
                        "id": len(users)+1,
                        "nome": nome_r,
                        "email": email_r,
                        "senha": senha_r,
                        "foto": caminho,
                        "role": role_novo,
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

# Promove automaticamente se for admin
if e_admin(usuario.get("email","")) and usuario.get("role") != "admin":
    usuario["role"] = "admin"
    users = load_users()
    for u in users:
        if u.get("id") == usuario.get("id"):
            u["role"] = "admin"
    save_users(users)
    st.session_state.usuario_logado = usuario

with st.sidebar:
    st.write("Meu Perfil")
    if usuario.get("foto") and os.path.exists(usuario["foto"]):
        st.image(usuario["foto"], width=150)
    st.write(f"**{usuario.get('nome','')}**")
    st.write(usuario.get("email",""))
    st.write(f"Role: {usuario.get('role','').upper()}")
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
        menu = st.radio("MENU ADMIN", ["Enviar Musica", "APROVACAO ADMIN", "Musicas no Ar", "TODAS CONTAS ARTISTAS"], key="menu_admin")
    else:
        menu = st.radio("MENU", ["Enviar Musica", "Musicas no Ar"], key="menu_art")

if menu == "Enviar Musica":
    st.subheader(f"Enviar musica - {usuario.get('nome','')}")
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
            st.success("Enviada! Aguardando aprovacao")
            st.balloons()

elif menu == "APROVACAO ADMIN":
    if usuario.get("role") != "admin":
        st.error("So admin")
        st.stop()
    st.subheader("APROVACAO - MUSICAS PENDENTES")
    musicas = load_musicas()
    pendentes = [m for m in musicas if m.get("status") == "PENDENTE"]
    st.metric("Pendentes", len(pendentes))
    if len(pendentes) == 0:
        st.info("Nenhuma musica pendente")
    for m in pendentes:
        with st.container():
            c1, c2 = st.columns([1,3])
            with c1:
                f = m.get("user_foto")
                if f and os.path.exists(f):
                    st.image(f, width=80)
                st.write(m.get("user_nome",""))
                st.caption(m.get("user_email",""))
            with c2:
                st.markdown(f"<div style='border:2px solid #FFD700; padding:10px; border-radius:10px; background:#1e1e1e;'><h4>{m.get('musica','')} - {m.get('artista','')}</h4><p>{m.get('genero','')} | {m.get('tipo','')} | {m.get('data','')}</p><p>{', '.join(m.get('plataformas',[]))}</p></div>", unsafe_allow_html=True)
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("APROVAR", key=f"ap_{m.get('id')}"):
                        for x in musicas:
                            if x.get("id") == m.get("id"):
                                x["status"] = "APROVADO"
                        save_musicas(musicas)
                        st.success("Aprovado!")
                        st.rerun()
                with col_b:
                    if st.button("REJEITAR", key=f"rej_{m.get('id')}"):
                        for x in musicas:
                            if x.get("id") == m.get("id"):
                                x["status"] = "REJEITADO"
                        save_musicas(musicas)
                        st.error("Rejeitado")
                        st.rerun()

elif menu == "TODAS CONTAS ARTISTAS":
    if usuario.get("role") != "admin":
        st.error("So admin pode ver")
        st.stop()
    st.subheader("TODAS CONTAS DOS ARTISTAS")
    users = load_users()
    artistas = [u for u in users if u.get("role") == "artist"]
    admins = [u for u in users if u.get("role") == "admin"]
    c1, c2, c3 = st.columns(3)
    c1.metric("Total", len(users))
    c2.metric("Artistas", len(artistas))
    c3.metric("Admins", len(admins))
    busca = st.text_input("Buscar por nome ou email")
    lista = users
    if busca:
        lista = [u for u in users if busca.lower() in u.get("nome","").lower() or busca.lower() in u.get("email","").lower()]
    st.markdown("### Fotos dos Artistas")
    cols = st.columns(3)
    for idx, u in enumerate(lista):
        with cols[idx % 3]:
            st.markdown("<div style='border:1px solid #FFD700; padding:10px; border-radius:10px; background:#1e1e1e; text-align:center; margin:5px;'>", unsafe_allow_html=True)
            f = u.get("foto")
            if f and os.path.exists(f):
                st.image(f, width=100)
            else:
                st.write("Sem foto")
            st.write(f"**{u.get('nome','')}**")
            st.caption(u.get("email",""))
            st.caption(f"{u.get('role','')} | {u.get('tipo_login','')} | {u.get('criado','')}")
            qtd = len([m for m in load_musicas() if m.get("user_id")==u.get("id")])
            st.write(f"Musicas: {qtd}")
            st.markdown("</div>", unsafe_allow_html=True)
    st.divider()
    tabela = []
    for u in lista:
        tabela.append({
            "ID": u.get("id"),
            "Nome": u.get("nome"),
            "Email": u.get("email"),
            "Foto": "SIM" if u.get("foto") else "NAO",
            "Tipo": u.get("tipo_login"),
            "Role": u.get("role"),
            "Criado": u.get("criado")
        })
    st.dataframe(tabela, use_container_width=True)

else:
    st.subheader("Musicas no Ar - Aprovadas")
    musicas = load_musicas()
    aprovadas = [m for m in musicas if m.get("status") == "APROVADO"]
    if usuario.get("role") != "admin":
        aprovadas = [m for m in aprovadas if m.get("user_id") == usuario.get("id")]
    if len(aprovadas) == 0:
        st.info("Nenhuma musica aprovada ainda")
    else:
        for m in aprovadas:
            st.markdown(f"<div style='border:1px solid #FFD700; padding:10px; border-radius:10px; margin:5px; background:#1a1a1a;'><h4>{m.get('musica','')} - {m.get('artista','')}</h4><p>{m.get('user_nome','')} | {m.get('genero','')} | {m.get('data','')}</p></div>", unsafe_allow_html=True)

st.sidebar.write("King-Slesha 2026 Matola")
