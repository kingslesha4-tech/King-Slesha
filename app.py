import streamlit as st, json, os, datetime

st.set_page_config(page_title="King Slesha Moz Distribution", page_icon="👑", layout="wide")

# ESCONDE TUDO
st.markdown("""
<style>
header, footer, #MainMenu {visibility: hidden;}
div[data-testid="stToolbar"] {display:none;}
.stAppDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

DB = "distro.json"
if not os.path.exists(DB):
    with open(DB,"w") as f: json.dump([],f)

def load():
    with open(DB,"r") as f: return json.load(f)
def save(d):
    with open(DB,"w") as f: json.dump(d,f,indent=2)

st.markdown("# 👑 KING SLESHA MOZ DISTRIBUTION")
st.markdown("### Lançamos tua música em 50+ plataformas: Spotify, Apple Music, Boomplay, TikTok, YouTube")
st.divider()

menu = st.sidebar.selectbox("Menu", ["🏠 Home", "🚀 Lançar Musica", "💳 Pagar 500MT", "📊 Meus Lancamentos", "🔐 Admin"])

if menu == "🏠 Home":
    c1,c2,c3 = st.columns(3)
    c1.metric("Plataformas", "50+")
    c2.metric("Artistas", len(load()))
    c3.metric("Comissao", "70% pra ti")
    st.markdown("""
    **Como funciona:**
    1. Paga 500MT via M-Pesa 853772668
    2. Preenche formulario em Lançar Musica
    3. Lancamos em 24h
    4. Recebes 70% todo dia 15 via M-Pesa
    
    **Plataformas:** Spotify, Apple Music, Boomplay, Audiomack, YouTube Music, TikTok, Instagram, Deezer, Tidal
    """)

elif menu == "🚀 Lançar Musica":
    st.markdown("### 📤 Formulario de Lancamento")
    with st.form("lancar"):
        nome_artista = st.text_input("Nome do Artista *")
        titulo = st.text_input("Titulo da Musica *")
        feat = st.text_input("Feat (opcional)")
        genero = st.selectbox("Genero", ["Hip Hop", "Trap", "Afrobeat", "Amapiano", "Kizomba", "Pandza", "R&B", "Outro"])
        compositor = st.text_input("Compositor *")
        data_lanc = st.date_input("Data desejada", min_value=datetime.date.today())
        capa = st.file_uploader("Capa 3000x3000 JPG *", type=["jpg","jpeg","png"])
        musica = st.file_uploader("Audio WAV ou MP3 *", type=["mp3","wav"])
        letra = st.text_area("Letra")
        tel = st.text_input("Teu WhatsApp * (84xxxxxxx)")
        id_mpesa = st.text_input("ID M-Pesa do pagamento 500MT *")
        submit = st.form_submit_button("ENVIAR", use_container_width=True)
        if submit:
            if nome_artista and titulo and compositor and musica and capa and tel and id_mpesa:
                novo = {
                    "id": len(load())+1,
                    "artista": nome_artista,
                    "titulo": titulo,
                    "feat": feat,
                    "genero": genero,
                    "compositor": compositor,
                    "data": str(data_lanc),
                    "tel": tel,
                    "id_mpesa": id_mpesa,
                    "status": "Pendente verificacao",
                    "data_envio": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "royalties": 0
                }
                db = load()
                db.append(novo)
                save(db)
                st.success(f"Recebido ID #{novo['id']}! Vamos verificar M-Pesa e lancar em 24h! WhatsApp {tel}")
                st.balloons()
            else:
                st.error("Preenche tudo com *")

elif menu == "💳 Pagar 500MT":
    st.markdown("### 💸 Pagar Lancamento - 500MT")
    st.info("Passo 1: Envia 500MT para M-Pesa 853772668 - Nome: KING SLESHA")
    st.info("Passo 2: Copia o ID da transacao e cola em Lancar Musica")
    st.link_button("📲 Avisar King no WhatsApp", "https://wa.me/258853772668?text=Quero%20pagar%20500MT%20para%20lancamento", use_container_width=True)

elif menu == "📊 Meus Lancamentos":
    tel = st.text_input("Escreve teu WhatsApp pra ver:")
    if tel:
        meus = [x for x in load() if x["tel"] == tel]
        if meus:
            for m in meus:
                with st.container(border=True):
                    st.write(f"#{m['id
