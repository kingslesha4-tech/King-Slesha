import streamlit as st, json, os, datetime

st.set_page_config(page_title="King Slesha Moz Distribution", page_icon="👑", layout="wide")
st.markdown("<style>header,footer,#MainMenu{visibility:hidden;}.stAppDeployButton{display:none;}</style>", unsafe_allow_html=True)

DB = "distro.json"
if not os.path.exists(DB):
    with open(DB,"w") as f: json.dump([],f)

def load(): 
    with open(DB,"r") as f: return json.load(f)
def save(d):
    with open(DB,"w") as f: json.dump(d,f,indent=2)

st.image("https://i.imgur.com/placeholder.png", width=0) # ignora

# HEADER
st.markdown("""
# 👑 KING SLESHA MOZ DISTRIBUTION
### Distribuidora Oficial de Moçambique - Para Spotify, Apple Music, Boomplay, TikTok, YouTube
""")
st.divider()

menu = st.sidebar.selectbox("Menu", ["🏠 Home", "🚀 Lançar Música", "📊 Meus Lançamentos", "💰 Royalties", "🔐 Admin Distro"])

if menu == "🏠 Home":
    c1,c2,c3 = st.columns(3)
    c1.metric("Plataformas", "50+")
    c2.metric("Artistas", len(load()))
    c3.metric("Comissão", "30% King / 70% Artista")
    st.markdown("""
    **Como funciona:**
    1. Tu envias música + capa + info aqui
    2. Nós revisamos em 24h
    3. Lançamos em Spotify, Apple Music, Boomplay, Audiomack, TikTok, Instagram, YouTube Music
    4. Tu recebes 70% dos lucros todo mês via M-Pesa 853772668
    
    **Preço:** 500MT por música ou 1000MT por álbum (até 10 músicas)
    **Paga via:** M-Pesa 853772668 / eMola 874336850
    """)
    st.link_button("🚀 Lançar minha música agora", "#", use_container_width=True)

elif menu == "🚀 Lançar Música":
    st.markdown("### 📤 Formulário de Lançamento")
    with st.form("lançar"):
        col1,col2 = st.columns(2)
        nome_artista = col1.text_input("Nome do Artista*")
        titulo = col2.text_input("Título da Música*")
        feat = st.text_input("Feat (opcional)")
        genero = st.selectbox("Gênero", ["Hip Hop", "Trap", "Afrobeat", "Amapiano", "Kizomba", "Pandza", "R&B", "Outro"])
        compositor = st.text_input("Compositor / Letrista*")
        data_lanc = st.date_input("Data de lançamento desejada", min_value=datetime.date.today())
        plataformas = st.multiselect("Plataformas", ["Spotify","Apple Music","Boomplay","Audiomack","YouTube Music","TikTok","Instagram","Deezer","Tidal"], default=["Spotify","Apple Music","Boomplay"])
        capa = st.file_uploader("Capa 3000x3000 JPG*", type=["jpg","jpeg","png"])
        musica = st.file_uploader("Áudio WAV ou MP3 320kbps*", type=["mp3","wav"])
        letra = st.text_area("Letra da música")
        tel = st.text_input("Teu WhatsApp* (84xxxxxxx)")
        id_mpesa = st.text_input("ID M-Pesa do pagamento 500MT*")

        submit = st.form_submit_button("🚀 ENVIAR PARA KING SLESHA MOZ", use_container_width=True)
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
                    "plataformas": plataformas,
                    "tel": tel,
                    "id_mpesa": id_mpesa,
                    "status": "⏳ Pendente verificação",
                    "data_envio": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "royalties": 0
                }
                db = load(); db.append(novo); save(db)
                st.success(f"Recebido! ID #{novo['id']} - Vamos verificar teu M-Pesa {id_mpesa} e lançar em 24h! Entraremos no WhatsApp {tel}")
                st.balloons()
            else:
                st.error("Preenche tudo que tem *")

elif menu == "📊 Meus Lançamentos":
    tel = st.text_input("Escreve teu WhatsApp pra ver teus lançamentos:")
    if tel:
        meus = [x for x in load() if x["tel"] == tel]
        if meus:
            for m in meus:
                with st.container(border=True):
                    st.write(f"**#{m['id']} - {m['titulo']} - {m['artista']}**")
                    st.write(f"Status: {m['status']} | Data: {m['data']} | Plataformas: {', '.join(m['plataformas'])}")
        else:
            st.info("Nada ainda com esse número")

elif menu == "💰 Royalties":
    st.markdown("### 💸 Como pagamos")
    st.write("Todo dia 15 pagamos via M-Pesa. 70% pra ti, 30% fica pra distribuição, marketing e registro.")
    st.write("Exemplo: Se tua música fez 10.000MT no Spotify, recebes 7.000MT")

elif menu == "🔐 Admin Distro":
    senha = st.text_input("Senha Admin", type="password")
    if senha == "king2024":
        db = load()
        st.write(f"Total lançamentos: {len(db)}")
        for m in db:
            with st.expander(f"#{m['id']} - {m['titulo']} - {m['artista']} - {m['status']}"):
                st.json(m)
                novo_status = st.selectbox(f"Atualizar status #{m['id']}", ["⏳ Pendente","✅ Aprovado - Enviado pra plataformas","🎉 No Ar!","❌ Rejeitado"], key=f"s{m['id']}")
                if st.button(f"Salvar status #{m['id']}", key=f"b{m['id']}"):
                    m["status"] = novo_status
                    save(db)
                    st.success("Atualizado!")

