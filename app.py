import streamlit as st, json, os, datetime

st.set_page_config(page_title="King Slesha Moz Distribution - Grátis", page_icon="👑", layout="centered")
st.markdown("<style>header,footer,#MainMenu{visibility:hidden;}div[data-testid='stToolbar']{display:none;}.stAppDeployButton{display:none;}</style>", unsafe_allow_html=True)

DB = "distro.json"
os.makedirs("musicas", exist_ok=True)
os.makedirs("capas", exist_ok=True)

if not os.path.exists(DB):
    with open(DB,"w") as f: json.dump([],f)

def load():
    with open(DB,"r") as f: return json.load(f)
def save(d):
    with open(DB,"w") as f: json.dump(d,f,indent=2)

# HEADER GRÁTIS
st.markdown("""
<div style="text-align:center; background:black; padding:25px; border-radius:20px;">
<h1 style="color:gold; margin:0;">👑 KING SLESHA MOZ</h1>
<h2 style="color:white; margin:0;">DISTRIBUTION</h2>
<p style="color:gold; font-size:18px; margin-top:10px;">🚀 100% GRÁTIS - Lança tua música agora!</p>
<p style="color:white;">Spotify | Apple Music | Boomplay | TikTok | YouTube Music + 45</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📤 Lançar Minha Música - Grátis")

with st.form("lancar"):
    nome_artista = st.text_input("Nome do Artista *")
    titulo = st.text_input("Título da Música *")
    feat = st.text_input("Feat (se tiver)")
    genero = st.selectbox("Gênero", ["Hip Hop","Trap","Afrobeat","Amapiano","Kizomba","Pandza","R&B","Marrabenta","Outro"])
    tel = st.text_input("Teu WhatsApp *")
    capa = st.file_uploader("Capa da música (foto 3000x3000) *", type=["jpg","png","jpeg"])
    musica = st.file_uploader("Tua música MP3 ou WAV *", type=["mp3","wav"])
    
    st.markdown("---")
    submit = st.form_submit_button("🚀 LANÇAR GRÁTIS AGORA", use_container_width=True)
    
    if submit:
        if nome_artista and titulo and tel and musica and capa:
            nome_arquivo = f"{nome_artista}_{titulo}".replace(" ", "_")
            path_musica = f"musicas/{nome_arquivo}.mp3"
            path_capa = f"capas/{nome_arquivo}.jpg"
            
            with open(path_musica, "wb") as f:
                f.write(musica.getbuffer())
            with open(path_capa, "wb") as f:
                f.write(capa.getbuffer())
            
            db = load()
            novo = {
                "id": len(db)+1,
                "artista": nome_artista,
                "titulo": titulo,
                "feat": feat,
                "genero": genero,
                "tel": tel,
                "status": "Recebido - Grátis",
                "data_envio": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                "path_musica": path_musica,
                "path_capa": path_capa
            }
            db.append(novo)
            save(db)
            st.success(f"✅ BOA {nome_artista}! Música '{titulo}' recebida! ID #{novo['id']}")
            st.success("Vamos lançar em 24h e te mandar link do Spotify no WhatsApp!")
            st.balloons()
        else:
            st.error("Preenche tudo com *")

st.divider()
st.markdown("<p style='text-align:center; color:gray;'>King Slesha Moz Distribution © 2026 - Matola | 100% Grátis para artistas de Moçambique 🇲🇿</p>", unsafe_allow_html=True)

# ADMIN ESCONDIDO - só tu
