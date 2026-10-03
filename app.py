import streamlit as st, json, os, datetime

st.set_page_config(page_title="King Slesha Moz Distribution", page_icon="👑", layout="centered")

st.markdown("<style>header,footer,#MainMenu{visibility:hidden;}div[data-testid='stToolbar']{display:none;}.stAppDeployButton{display:none;}</style>", unsafe_allow_html=True)

DB = "distro.json"
if not os.path.exists(DB):
    with open(DB,"w") as f: json.dump([],f)
def load():
    with open(DB,"r") as f: return json.load(f)
def save(d):
    with open(DB,"w") as f: json.dump(d,f,indent=2)

# HEADER PREMIUM
st.markdown("""
<div style="text-align:center; background:black; padding:20px; border-radius:15px;">
<h1 style="color:gold; margin:0;">👑 KING SLESHA MOZ</h1>
<h3 style="color:white; margin:0;">DISTRIBUTION</h3>
<p style="color:gold;">A Primeira Distribuidora de Maputo para o Mundo</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🚀 Lançamos em 50+ plataformas")
st.write("Spotify | Apple Music | Boomplay | Audiomack | TikTok | YouTube Music | Deezer | Tidal")

menu = st.sidebar.selectbox("Menu", ["Home", "Lancar Musica", "Pagar 500MT", "Meus Lancamentos", "Admin"])

if menu == "Home":
    c1,c2,c3 = st.columns(3)
    c1.metric("Plataformas", "50+")
    c2.metric("Artistas", len(load()))
    c3.metric("Comissao", "70% pra ti")
    st.success("Como funciona: 1. Paga 500MT via M-Pesa 853772668 | 2. Preenche formulario | 3. Lancamos em 24h | 4. Recebes 70% todo dia 15 via M-Pesa")
    st.link_button("🚀 LANCAR MINHA MUSICA AGORA", "https://zpjg.streamlit.app/?embed=true", use_container_width=True)

elif menu == "Lancar Musica":
    st.markdown("### 📤 Formulario")
    with st.form("lancar"):
        nome_artista = st.text_input("Nome do Artista *")
        titulo = st.text_input("Titulo *")
        feat = st.text_input("Feat")
        genero = st.selectbox("Genero", ["Hip Hop","Trap","Afrobeat","Amapiano","Kizomba","Pandza","R&B"])
        compositor = st.text_input("Compositor *")
        data_lanc = st.date_input("Data lancamento", min_value=datetime.date.today())
        capa = st.file_uploader("Capa 3000x3000 *", type=["jpg","png","jpeg"])
        musica = st.file_uploader("Audio MP3/WAV *", type=["mp3","wav"])
        tel = st.text_input("WhatsApp *")
        id_mpesa = st.text_input("ID M-Pesa 500MT *")
        submit = st.form_submit_button("ENVIAR PARA DISTRIBUICAO", use_container_width=True)
        if submit:
            if nome_artista and titulo and compositor and musica and capa and tel and id_mpesa:
                db = load()
                novo = {"id": len(db)+1, "artista": nome_artista, "titulo": titulo, "feat": feat, "genero": genero, "compositor": compositor, "data": str(data_lanc), "tel": tel, "id_mpesa": id_mpesa, "status": "Pendente", "data_envio": datetime.datetime.now().strftime("%d/%m/%Y"), "royalties": 0}
                db.append(novo); save(db)
                st.success("Enviado ID "+str(novo["id"])+"! Verificamos M-Pesa em breve!")
                st.balloons()
            else:
                st.error("Preenche com *")

elif menu == "Pagar 500MT":
    st.markdown("### 💸 Pagamento")
    st.warning("M-Pesa: 853772668 - KING SLESHA - 500MT por musica")
    st.link_button("📲 Confirmar no WhatsApp", "https://wa.me/258853772668?text=Paguei%20500MT%20ID:", use_container_width=True)

elif menu == "Meus Lancamentos":
    tel = st.text_input("Teu WhatsApp:")
    if tel:
        for m in [x for x in load() if x["tel"]==tel]:
            with st.container(border=True):
                st.write(m["titulo"]+" - "+m["artista"]+" | Status: "+m["status"])

elif menu == "Admin":
    s = st.text_input("Senha", type="password")
    if s == "king2024":
        for m in load():
            st.write(str(m["id"])+" - "+m["titulo"]+" - "+m["tel"]+" - "+m["id_mpesa"])
