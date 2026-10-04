import streamlit as st
import datetime, random, string
from supabase import create_client

SUPABASE_URL = "https://hfjskhhjrdjuphkbjdpu.supabase.co"
SUPABASE_KEY = "sb_publishable_gBj-IUXwTe8E1olKTLRBhg_l87QRjXu"

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)
supabase = get_supabase()

st.set_page_config(page_title="KING SLESHA DISTRO", page_icon="👑", layout="centered")
st.markdown("""
<div style="text-align:center;background:black;padding:20px;border-radius:15px;border:3px solid #1DB954;">
<h1 style="color:#1DB954;">👑 KING SLESHA MOZ</h1>
<p style="color:white;">DISTRIBUIDORA OFICIAL - APROVAÇÃO KING</p>
<p style="color:#1DB954;">🎧 SPOTIFY + 📺 YOUTUBE = MESMA MÚSICA APROVADA</p>
</div><br>""", unsafe_allow_html=True)

def gen_codes():
    isrc = f"MZ-{''.join(random.choices(string.ascii_uppercase, k=3))}-{datetime.datetime.now().year}-{''.join(random.choices(string.digits, k=5))}"
    upc = ''.join(random.choices(string.digits, k=12))
    return isrc, upc

def upload_file(bucket, file):
    try:
        name = f"{datetime.datetime.now().timestamp()}_{file.name.replace(' ','_')}"
        supabase.storage.from_(bucket).upload(name, file.getvalue(), {"content-type": file.type})
        return supabase.storage.from_(bucket).get_public_url(name)
    except: return None

def listar():
    try:
        res = supabase.table("musicas").select("*").order("created_at", desc=True).execute()
        return res.data
    except: return []

menu = st.selectbox("MENU", ["🏠 CATÁLOGO PÚBLICO", "🚀 SOU ARTISTA - LANÇAR", "🔐 PAINEL KING - SÓ DONO"])

if menu == "🏠 CATÁLOGO PÚBLICO":
    musicas = listar()
    aprovadas = [m for m in musicas if m.get('status')=='aprovada']
    if not aprovadas:
        st.info("Nenhuma música aprovada ainda")
    else:
        tab1, tab2 = st.tabs(["🎧 SPOTIFY", "📺 YOUTUBE"])
        with tab1:
            st.subheader(f"{len(aprovadas)} músicas no Spotify")
            for m in aprovadas:
                with st.container(border=True):
                    c1,c2 = st.columns([1,2])
                    with c1:
                        if m.get('capa_url'): st.image(m['capa_url'], use_container_width=True)
                        else: st.write("🎵")
                    with c2:
                        st.markdown(f"**{m['titulo']}**")
                        st.write(m['artista'])
                        st.caption(f"ISRC {m['isrc']}")
                        if m.get('audio_url'): st.audio(m['audio_url'])
        with tab2:
            st.subheader(f"{len(aprovadas)} vídeos no YouTube (mesmas músicas)")
            for m in aprovadas:
                with st.container(border=True):
                    if m.get('capa_url'): st.image(m['capa_url'], use_container_width=True)
                    st.markdown(f"**{m['titulo']}** - {m['artista']}")
                    if m.get('audio_url'): 
                        st.audio(m['audio_url'])
                        st.caption("📺 Player YouTube da Distribuidora")

elif menu == "🚀 SOU ARTISTA - LANÇAR":
    st.markdown("### 🚀 Enviar música pro King aprovar")
    st.info("Você envia, o King Slesha ouve e aprova. Depois fica no Spotify e YouTube da distribuidora automaticamente.")
    titulo = st.text_input("Título da música *")
    artista = st.text_input("Teu nome artístico *")
    tel = st.text_input("Teu WhatsApp *")
    f = st.file_uploader("Tua música MP3/WAV *", type=['mp3','wav','m4a'])
    capa = st.file_uploader("Tua capa 3000x3000 (recomendado)", type=['jpg','jpeg','png'])
    
    if st.button("📤 ENVIAR PRO KING OUVIR E APROVAR 👑", type="primary", use_container_width=True):
        if not titulo or not artista or not tel or not f:
            st.error("Preenche título, artista, WhatsApp e música!")
        else:
            isrc, upc = gen_codes()
            with st.spinner("Enviando..."):
                audio_url = upload_file("musicas", f)
                capa_url = upload_file("capas", capa) if capa else None
            if not audio_url:
                st.error("Erro upload. Tenta novamente")
            else:
                data = {"titulo":titulo,"artista":artista,"tel":tel,"status":"pendente","data_envio":datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),"isrc":isrc,"upc":upc,"audio_url":audio_url,"capa_url":capa_url}
                supabase.table("musicas").insert(data).execute()
                st.success("✅ Enviado! O King vai ouvir e aprovar.")
                st.caption(f"ISRC: {isrc} - Aguarde no WhatsApp {tel}")
                if capa_url: st.image(capa_url, width=200)
                st.audio(audio_url)
                st.balloons()

else:
    senha = st.text_input("Senha do Dono", type="password")
    if senha=="king2024":
        st.success("👑 KING - Ouça antes de aprovar")
        musicas = listar()
        pendentes = [m for m in musicas if m.get('status')=='pendente']
        aprovadas = [m for m in musicas if m.get('status')=='aprovada']
        c1,c2 = st.columns(2)
        c1.metric("Pendentes pra ouvir", len(pendentes))
        c2.metric("Aprovadas", len(aprovadas))
        for m in pendentes:
            with st.container(border=True):
                st.markdown(f"### 🎵 {m['titulo']} - {m['artista']}")
                st.write(f"📱 {m['tel']} | {m['data_envio']}")
                if m.get('capa_url'): st.image(m['capa_url'], width=200)
                # AQUI TU OUVES!
                if m.get('audio_url'):
                    st.markdown("**🔊 OUVE AQUI ANTES DE APROVAR:**")
                    st.audio(m['audio_url'])
                else:
                    st.warning("Sem áudio (música antiga)")
                col1,col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ APROVAR - VAI PRO SPOTIFY E YOUTUBE", key=f"ap{m['id']}", use_container_width=True):
                        supabase.table("musicas").update({"status":"aprovada"}).eq("id", m['id']).execute()
                        st.success("Aprovada! Agora no Spotify e YouTube!")
                        st.rerun()
                with col2:
                    if st.button(f"❌ REJEITAR", key=f"rj{m['id']}", use_container_width=True):
                        supabase.table("musicas").delete().eq("id", m['id']).execute()
                        st.rerun()
    elif senha:
        st.error("Senha errada")
