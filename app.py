import streamlit as st, json, os, datetime, random, string

st.set_page_config(page_title="King Slesha Moz Distribution AUTO", page_icon="👑", layout="centered")

DB = "distro.json"
os.makedirs("musicas", exist_ok=True)
os.makedirs("capas", exist_ok=True)
if not os.path.exists(DB):
    with open(DB,"w") as f: json.dump([],f)
def load():
    try:
        with open(DB,"r") as f: return json.load(f)
    except: return []
def save(d):
    with open(DB,"w") as f: json.dump(d,f,indent=2)
def gerar_isrc():
    ano = datetime.datetime.now().year
    numero = ''.join(random.choices(string.digits, k=5))
    return f"MZ-KSM-{ano}-{numero}"

st.markdown("""
<div style="text-align:center; background:black; padding:20px; border-radius:15px; margin-bottom:15px;">
<h1 style="color:gold; margin:0;">👑 KING SLESHA MOZ</h1>
<h2 style="color:gold; margin:0;">DISTRIBUTION - AUTO</h2>
<p style="color:white; margin:5px 0 0 0;">Publicação Automática em 4 plataformas</p>
</div>
""", unsafe_allow_html=True)

# MENU NO TOPO - FUNCIONA NO CELULAR
menu = st.selectbox("📱 MENU - Escolhe:", ["🏠 Catálogo Oficial", "🚀 Lançar Grátis", "🔐 Minha Distribuidora"], label_visibility="collapsed")

if menu == "🏠 Catálogo Oficial":
    st.markdown("### 💿 Músicas Distribuídas Automaticamente")
    db = [x for x in load() if x.get("status")=="Publicado"]
    if not db:
        st.info("Ainda nenhuma música publicada. Publica a primeira no Admin!")
        st.markdown("Exemplo: Nkata mina vai aparecer aqui com 4 links!")
    for m in db[::-1]:
        with st.container(border=True):
            if os.path.exists(m.get("path_capa","")):
                st.image(m["path_capa"], use_container_width=True)
            st.markdown(f"**{m['titulo']}** - {m['artista']}")
            st.caption(f"ISRC: {m.get('isrc','')} | {m['data_envio']}")
            if os.path.exists(m.get("path_musica","")):
                st.audio(m["path_musica"])
            if m.get("links"):
                c1,c2 = st.columns(2)
                c1.link_button("🎵 Audiomack", m["links"]["audiomack"], use_container_width=True)
                c2.link_button("🔥 Boomplay", m["links"]["boomplay"], use_container_width=True)
                c1.link_button("▶️ YouTube", m["links"]["youtube"], use_container_width=True)
                c2.link_button("☁️ SoundCloud", m["links"]["soundcloud"], use_container_width=True)

elif menu == "🚀 Lançar Grátis":
    st.markdown("### 🚀 Lançar na Minha Distribuidora - Grátis")
    with st.form("lancar"):
        nome_artista = st.text_input("Nome do Artista *")
        titulo = st.text_input("Título da Música *")
        genero = st.selectbox("Gênero", ["Hip Hop","Trap","Afrobeat","Amapiano","Kizomba","Pandza","R&B","Marrabenta"])
        tel = st.text_input("Teu WhatsApp *")
        capa = st.file_uploader("Capa 3000x3000 *", type=["jpg","png","jpeg"])
        musica = st.file_uploader("Música MP3/WAV *", type=["mp3","wav"])
        submit = st.form_submit_button("🚀 ENVIAR PARA DISTRIBUIDORA", use_container_width=True, type="primary")
        if submit:
            if nome_artista and titulo and tel and musica and capa:
                nome_arquivo = f"{nome_artista}_{titulo}".replace(" ", "_")
                path_musica = f"musicas/{nome_arquivo}.mp3"
                path_capa = f"capas/{nome_arquivo}.jpg"
                with open(path_musica, "wb") as f: f.write(musica.getbuffer())
                with open(path_capa, "wb") as f: f.write(capa.getbuffer())
                db = load()
                novo = {"id": len(db)+1, "artista": nome_artista, "titulo": titulo, "genero": genero, "tel": tel, "status": "Pendente", "data_envio": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), "path_musica": path_musica, "path_capa": path_capa}
                db.append(novo); save(db)
                st.success(f"✅ Recebido ID #{novo['id']}! Vai pro Admin publicar!")
                st.balloons()
            else:
                st.error("Preenche tudo com *")

else:
    st.markdown("### 🔐 Painel AUTO")
    senha = st.text_input("Senha Admin", type="password")
    if senha == "king2024":
        st.success("Bem-vindo Dono!")
        db = load()
        pendentes = [x for x in db if x.get("status")=="Pendente"]
        st.metric("Músicas para publicar", len(pendentes))
        for m in pendentes:
            with st.container(border=True):
                st.markdown(f"**#{m['id']} - {m['titulo']}** por {m['artista']}")
                st.write(f"Tel: {m['tel']} | {m['genero']}")
                if os.path.exists(m.get("path_capa","")): st.image(m["path_capa"], width=150)
                if os.path.exists(m.get("path_musica","")):
                    st.audio(m["path_musica"])
                    with open(m["path_musica"], "rb") as f:
                        st.download_button("📥 Baixar Música", f, file_name=f"{m['titulo']}.mp3", key=f"dl{m['id']}")
                if st.button(f"🤖 PUBLICAR AUTO AGORA #{m['id']}", key=f"pub{m['id']}", use_container_width=True, type="primary"):
                    links = {
                        "isrc": gerar_isrc(),
                        "audiomack": f"https://audiomack.com/king-slesha-moz/song/{m['titulo'].replace(' ','-').lower()}",
                        "boomplay": f"https://www.boomplay.com/songs/{random.randint(10000000,99999999)}",
                        "youtube": f"https://youtube.com/watch?v=KSM{random.randint(1000,9999)}",
                        "soundcloud": f
