import streamlit as st, datetime, random, string, requests, os, tempfile
from supabase import create_client
from PIL import Image

SUPABASE_URL = "https://hfjskhhjrdjuphkbjdpu.supabase.co"
SUPABASE_KEY = "sb_publishable_gBj-IUXwTe8E1olKTLRBhg_l87QRjXu"

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)
supabase = get_supabase()

st.set_page_config(page_title="KING V12 VIDEO", page_icon="👑", layout="centered")
st.markdown("""<div style="text-align:center;background:black;padding:20px;border-radius:15px;border:3px solid red;">
<h1 style="color:#1DB954;">👑 KING V12 - GERA VÍDEO</h1><p style="color:white;">Aprova > Baixa Vídeo > Posta no YouTube REAL</p></div><br>""", unsafe_allow_html=True)

def gen_codes():
    return f"MZ-{''.join(random.choices(string.ascii_uppercase, k=3))}-{datetime.datetime.now().year}-{''.join(random.choices(string.digits, k=5))}", ''.join(random.choices(string.digits, k=12))

def upload_file(bucket, file):
    try:
        name = f"{datetime.datetime.now().timestamp()}_{file.name.replace(' ','_')}"
        supabase.storage.from_(bucket).upload(name, file.getvalue(), {"content-type": file.type})
        return supabase.storage.from_(bucket).get_public_url(name)
    except: return None

def listar():
    try: return supabase.table("musicas").select("*").order("created_at", desc=True).execute().data
    except: return []

def gerar_video(audio_url, capa_url, titulo):
    try:
        from moviepy.editor import AudioFileClip, ImageClip
        # baixa audio e capa temp
        tmpdir = tempfile.mkdtemp()
        audio_path = os.path.join(tmpdir, "audio.mp3")
        capa_path = os.path.join(tmpdir, "capa.jpg")
        video_path = os.path.join(tmpdir, f"{titulo}.mp4")
        
        with open(audio_path, "wb") as f:
            f.write(requests.get(audio_url).content)
        with open(capa_path, "wb") as f:
            f.write(requests.get(capa_url).content)
        
        audio = AudioFileClip(audio_path)
        # resize capa pra 1280x720
        img = Image.open(capa_path).convert("RGB")
        img = img.resize((1280,720))
        img.save(capa_path)
        
        clip = ImageClip(capa_path, duration=audio.duration)
        clip = clip.set_audio(audio)
        clip.write_videofile(video_path, fps=24, codec='libx264', audio_codec='aac')
        return video_path
    except Exception as e:
        st.error(f"Erro gerar vídeo: {e} - Instala moviepy no requirements.txt")
        return None

menu = st.selectbox("MENU", ["🏠 CATÁLOGO", "🚀 SOU ARTISTA", "🔐 PAINEL KING"])

if menu == "🏠 CATÁLOGO":
    aprovadas = [m for m in listar() if m.get('status')=='aprovada']
    t1,t2 = st.tabs(["🎧 Spotify", "📺 YouTube do Site"])
    with t1:
        for m in aprovadas:
            with st.container(border=True):
                c1,c2 = st.columns([1,2])
                with c1:
                    if m.get('capa_url'): st.image(m['capa_url'], use_container_width=True)
                with c2:
                    st.write(f"**{m['titulo']}** - {m['artista']}")
                    if m.get('audio_url'): st.audio(m['audio_url'])
    with t2:
        for m in aprovadas:
            with st.container(border=True):
                if m.get('capa_url'): st.image(m['capa_url'], use_container_width=True)
                st.write(f"**{m['titulo']}** - {m['artista']}")
                if m.get('audio_url'): st.audio(m['audio_url'])

elif menu == "🚀 SOU ARTISTA":
    titulo = st.text_input("Título *")
    artista = st.text_input("Artista *")
    tel = st.text_input("WhatsApp *")
    f = st.file_uploader("Música MP3 *", type=['mp3','wav','m4a'])
    capa = st.file_uploader("Capa JPG *", type=['jpg','jpeg','png'])
    if st.button("ENVIAR PRO KING 👑", type="primary", use_container_width=True):
        if not titulo or not artista or not tel or not f:
            st.error("Preenche tudo!")
        else:
            isrc, upc = gen_codes()
            with st.spinner("Enviando..."):
                audio_url = upload_file("musicas", f)
                capa_url = upload_file("capas", capa) if capa else None
            if audio_url:
                supabase.table("musicas").insert({"titulo":titulo,"artista":artista,"tel":tel,"status":"pendente","data_envio":datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),"isrc":isrc,"upc":upc,"audio_url":audio_url,"capa_url":capa_url}).execute()
                st.success(f"Enviado! ISRC {isrc} - King vai ouvir")
                if capa_url: st.image(capa_url, width=200)
                st.audio(audio_url)
                st.balloons()

else:
    senha = st.text_input("Senha Dono", type="password")
    if senha=="king2024":
        pendentes = [m for m in listar() if m.get('status')=='pendente']
        st.metric("Pra ouvir e aprovar", len(pendentes))
        for m in pendentes:
            with st.container(border=True):
                st.markdown(f"### {m['titulo']} - {m['artista']} | {m['tel']}")
                if m.get('capa_url'): st.image(m['capa_url'], width=200)
                if m.get('audio_url'):
                    st.markdown("**🔊 OUVE AQUI:**")
                    st.audio(m['audio_url'])
                
                col1,col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ APROVAR", key=f"ap{m['id']}", use_container_width=True):
                        supabase.table("musicas").update({"status":"aprovada"}).eq("id", m['id']).execute()
                        st.rerun()
                with col2:
                    if st.button(f"❌ REJEITAR", key=f"rj{m['id']}", use_container_width=True):
                        supabase.table("musicas").delete().eq("id", m['id']).execute()
                        st.rerun()

        st.divider()
        st.subheader("📺 GERAR VÍDEO PRO YOUTUBE REAL")
        aprovadas = [m for m in listar() if m.get('status')=='aprovada']
        for m in aprovadas:
            with st.container(border=True):
                st.write(f"**{m['titulo']}** - {m['artista']}")
                if m.get('capa_url'): st.image(m['capa_url'], width=150)
                if st.button(f"🎬 GERAR VÍDEO MP4", key=f"vid{m['id']}"):
                    if not m.get('audio_url') or not m.get('capa_url'):
                        st.error("Precisa áudio + capa pra gerar vídeo")
                    else:
                        with st.spinner("Gerando vídeo... 30seg"):
                            path = gerar_video(m['audio_url'], m['capa_url'], m['titulo'])
                        if path and os.path.exists(path):
                            with open(path, "rb") as f:
                                st.download_button(f"📥 BAIXAR {m['titulo']}.mp4", f, file_name=f"{m['titulo']}.mp4", mime="video/mp4", key=f"down{m['id']}")
                            st.success("Vídeo pronto! Baixa e posta no teu canal YouTube: King Slesha Moz Distribution")
    elif senha:
        st.error("Senha errada")
