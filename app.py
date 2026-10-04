import streamlit as st
import datetime, random, string
from supabase import create_client

SUPABASE_URL = "https://hfjskhhjrdjuphkbjdpu.supabase.co"
SUPABASE_KEY = "sb_publishable_gBj-IUXwTe8E1olKTLRBhg_l87QRjXu"

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)
supabase = get_supabase()

st.set_page_config(page_title="KING SLESHA MOZ V9", page_icon="👑", layout="centered")
st.markdown("""<div style="text-align:center;background:black;padding:20px;border-radius:15px;border:2px solid #FF0000;">
<h1 style="color:#1DB954;">👑 KING SLESHA MOZ V9</h1><p style="color:white;">🎧 SPOTIFY + 📺 YOUTUBE + NUNCA APAGA</p></div>""", unsafe_allow_html=True)

def gen_codes():
    isrc = f"MZ-{''.join(random.choices(string.ascii_uppercase, k=3))}-{datetime.datetime.now().year}-{''.join(random.choices(string.digits, k=5))}"
    upc = ''.join(random.choices(string.digits, k=12))
    return isrc, upc

def upload_file(bucket, file):
    try:
        name = f"{datetime.datetime.now().timestamp()}_{file.name}"
        supabase.storage.from_(bucket).upload(name, file.getvalue(), {"content-type": file.type})
        return supabase.storage.from_(bucket).get_public_url(name)
    except: return None

def listar():
    try:
        res = supabase.table("musicas").select("*").order("created_at", desc=True).execute()
        return res.data
    except: return []

def youtube_id(url):
    if not url: return None
    if "youtu.be/" in url: return url.split("youtu.be/")[-1].split("?")[0]
    if "v=" in url: return url.split("v=")[-1].split("&")[0]
    return url

menu = st.selectbox("Navegação", ["🏠 Catálogo Spotify + YouTube", "🚀 Lançar no Spotify AUTO", "🔐 Painel Spotify Provider"])

if menu == "🏠 Catálogo Spotify + YouTube":
    st.subheader("🔥 Tudo em um só lugar")
    tab1, tab2 = st.tabs(["🎧 Músicas", "📺 Vídeos YouTube"])
    musicas = listar()
    aprovadas = [m for m in musicas if m.get('status')=='aprovada']

    with tab1:
        for m in aprovadas:
            col1, col2 = st.columns([1,2])
            with col1:
                if m.get('capa_url'): st.image(m['capa_url'], use_container_width=True)
                else: st.write("🎵")
            with col2:
                st.markdown(f"**{m['titulo']}** - {m['artista']}")
                st.caption(f"ISRC: {m['isrc']}")
                if m.get('audio_url'): st.audio(m['audio_url'])
                if m.get('youtube_url'):
                    st.link_button("▶️ Ver no YouTube", m['youtube_url'])
            st.divider()

    with tab2:
        for m in aprovadas:
            if m.get('youtube_url'):
                yt = youtube_id(m['youtube_url'])
                st.markdown(f"**{m['titulo']}** - {m['artista']}")
                st.video(f"https://www.youtube.com/watch?v={yt}")
                if m.get('capa_url'):
                    col_a, col_b = st.columns(2)
                    with col_a: st.image(m['capa_url'], width=150)
                    with col_b:
                        if m.get('audio_url'): st.audio(m['audio_url'])
                st.divider()
        if not any(m.get('youtube_url') for m in aprovadas):
            st.info("Nenhum vídeo YouTube ainda. Lança com link YouTube!")

elif menu == "🚀 Lançar no Spotify AUTO":
    st.subheader("🚀 Lançar com YouTube também")
    titulo = st.text_input("Título *")
    artista = st.text_input("Artista *")
    tel = st.text_input("Teu WhatsApp *")
    youtube_url = st.text_input("Link YouTube (opcional) - ex: https://youtu.be/xxxxx")
    st.caption("👆 Se já tens vídeo no YouTube, cola o link aqui!")
    f = st.file_uploader("Música MP3/WAV *", type=['mp3','wav','m4a'])
    capa = st.file_uploader("Capa 3000x3000", type=['jpg','jpeg','png'])

    if st.button("ENVIAR PARA ANÁLISE 👑"):
        if not titulo or not artista or not tel or not f:
            st.error("❌ Preenche Título, Artista, WhatsApp e Música!")
        else:
            isrc, upc = gen_codes()
            with st.spinner("Subindo..."):
                audio_url = upload_file("musicas", f)
                capa_url = upload_file("capas", capa) if capa else None
            data = {"titulo":titulo,"artista":artista,"tel":tel,"status":"pendente","data_envio":datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),"isrc":isrc,"upc":upc,"audio_url":audio_url,"capa_url":capa_url,"youtube_url":youtube_url}
            supabase.table("musicas").insert(data).execute()
            st.success(f"✅ Recebido! ISRC: {isrc}")
            if capa_url: st.image(capa_url, width=200)
            if audio_url: st.audio(audio_url)
            if youtube_url:
                st.video(youtube_url)
            st.balloons()
            st.info("Vai no Painel king2024 pra aprovar!")

else:
    senha = st.text_input("Senha Provider", type="password")
    if senha=="king2024":
        st.success("✅ PAINEL V9 - SPOTIFY + YOUTUBE")
        musicas = listar()
        st.metric("Na fila", len([m for m in musicas if m['status']=='pendente']))
        for m in musicas:
            if m['status']=='pendente':
                st.write(f"--- 🎵 **{m['titulo']}** - {m['artista']}")
                if m.get('capa_url'): st.image(m['capa_url'], width=150)
                if m.get('audio_url'): st.audio(m['audio_url'])
                if m.get('youtube_url'): st.video(m['youtube_url'])
                col1,col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ APROVAR {m['id']}", key=f"ap{m['id']}"):
                        supabase.table("musicas").update({"status":"aprovada"}).eq("id", m['id']).execute()
                        st.rerun()
                with col2:
                    if st.button(f"❌ REJEITAR {m['id']}", key=f"rj{m['id']}"):
                        supabase.table("musicas").delete().eq("id", m['id']).execute()
                        st.rerun()
    elif senha: st.error("Senha errada")
