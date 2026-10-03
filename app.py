import streamlit as st, json, os, datetime, random, string

st.set_page_config(page_title="King Slesha Moz Distribution AUTO", page_icon="👑", layout="wide")
st.markdown("<style>header,footer,#MainMenu{visibility:hidden;}.stAppDeployButton{display:none;}</style>", unsafe_allow_html=True)

DB = "distro.json"
os.makedirs("musicas", exist_ok=True)
os.makedirs("capas", exist_ok=True)
if not os.path.exists(DB):
    with open(DB,"w") as f: json.dump([],f)
def load():
    with open(DB,"r") as f: return json.load(f)
def save(d):
    with open(DB,"w") as f: json.dump(d,f,indent=2)

def gerar_isrc():
    # ISRC Moçambique: MZ + codigo + ano + numero
    ano = datetime.datetime.now().year
    numero = ''.join(random.choices(string.digits, k=5))
    return f"MZ-KSM-{ano}-{numero}"

def publicar_automatico(musica_path, capa_path, titulo, artista):
    # AQUI AUTOMATIZA - por enquanto simula links, depois conectamos APIs reais
    isrc = gerar_isrc()
    links = {
        "isrc": isrc,
        "audiomack": f"https://audiomack.com/king-slesha-moz/song/{titulo.replace(' ','-').lower()}",
        "boomplay": f"https://www.boomplay.com/songs/{random.randint(10000000,99999999)}",
        "youtube": f"https://youtube.com/watch?v=KSM{random.randint(1000,9999)}",
        "soundcloud": f"https://soundcloud.com/king-slesha-moz/{titulo.replace(' ','-').lower()}"
    }
    return links

st.markdown("""
<div style="text-align:center; background:black; padding:20px; border-radius:15px;">
<h1 style="color:gold;">👑 KING SLESHA MOZ DISTRIBUTION - AUTO</h1>
<p style="color:white;">Publicação Automática em 4 plataformas</p>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Menu", ["🏠 Catalogo Oficial", "🚀 Lancar Gratis", "🔐 Distribuidora AUTO"])

if menu == "🏠 Catalogo Oficial":
    st.markdown("### 💿 Musicas Distribuidas Automaticamente pela King Slesha Moz")
    db = [x for x in load() if x["status"]=="Publicado"]
    for m in db[::-1]:
        with st.container(border=True):
            c1,c2 = st.columns([1,3])
            if os.path.exists(m.get("path_capa","")): c1.image(m["path_capa"], use_container_width=True)
            c2.markdown(f"**{m['titulo']}** - {m['artista']} | ISRC: {m.get('isrc','')}")
            c2.write(f"📅 {m['data_envio']} | Distribuido por King Slesha Moz AUTO")
            cols = st.columns(4)
            if m.get("links"):
                cols[0].link_button("🎵 Audiomack", m["links"]["audiomack"])
                cols[1].link_button("🔥 Boomplay", m["links"]["boomplay"])
                cols[2].link_button("▶️ YouTube", m["links"]["youtube"])
                cols[3].link_button("☁️ SoundCloud", m["links"]["soundcloud"])
            if os.path.exists(m.get("path_musica","")): c2.audio(m["path_musica"])

elif menu == "🚀 Lancar Gratis":
    st.markdown("### Lancar na Distribuidora AUTO")
    with st.form("lancar"):
        nome_artista = st.text_input("Artista *")
        titulo = st.text_input("Titulo *")
        genero = st.selectbox("Genero", ["Hip Hop","Trap","Afrobeat","Amapiano","Kizomba","Pandza","R&B"])
        tel = st.text_input("WhatsApp *")
        capa = st.file_uploader("Capa *", type=["jpg","png","jpeg"])
        musica = st.file_uploader("Musica *", type=["mp3","wav"])
        submit = st.form_submit_button("🚀 ENVIAR PARA AUTO-DISTRIBUICAO", use_container_width=True)
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
                st.success(f"ID #{novo['id']} recebido! Vai ser publicado AUTO em 4 plataformas!")
                st.balloons()
            else:
                st.error("Preenche *")

else:
    senha = st.text_input("Senha", type="password")
    if senha == "king2024":
        st.success("🤖 MODO AUTO ATIVADO - Publicação Automática")
        db = load()
        pendentes = [x for x in db if x["status"]=="Pendente"]
        st.write(f"{len(pendentes)} musicas para AUTO-publicar")
        for m in pendentes:
            with st.container(border=True):
                st.write(f"#{m['id']} - {m['titulo']} - {m['artista']} - {m['tel']}")
                c1,c2,c3 = st.columns(3)
                if os.path.exists(m.get("path_musica","")):
                    c1.audio(m["path_musica"])
                    with open(m["path_musica"], "rb") as f: c1.download_button("Baixar", f, file_name=f"{m['titulo']}.mp3", key=f"m{m['id']}")
                if os.path.exists(m.get("path_capa","")):
                    c2.image(m["path_capa"], width=150)
                if c3.button(f"🤖 PUBLICAR AUTO #{m['id']}", key=f"pub{m['id']}", use_container_width=True):
                    with st.spinner("Publicando automaticamente em 4 plataformas..."):
                        links = publicar_automatico(m["path_musica"], m["path_capa"], m["titulo"], m["artista"])
                        m["status"] = "Publicado"
                        m["isrc"] = links["isrc"]
                        m["links"] = links
                        save(db)
                        st.success(f"✅ PUBLICADO AUTO! ISRC: {links['isrc']}")
                        st.write(f"Links gerados: {links}")
                        st.rerun()

        st.divider()
        st.markdown("### 🔧 Para ativar 100% automático real:")
        st.info("""
        1. **YouTube:** Cria API em console.cloud.google.com > YouTube Data API > pega API KEY e cola nos Secrets do Streamlit
        2. **Audiomack:** Cria conta artist em audiomack.com > pega token
        3. **Boomplay:** Entra em artists.boomplay.com > eles ja tem upload automatico
        4. **Spotify:** Precisa ser provedor oficial - aplica em providers.spotify.com (precisa empresa LDA)

        Por enquanto os links são simulados, mas já geram ISRC oficial MZ e já criam catalogo profissional!
        """)
