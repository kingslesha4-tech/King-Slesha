import streamlit as st
import datetime, random, string
from supabase import create_client

SUPABASE_URL = "https://hfjskhhjrdjuphkbjdpu.supabase.co"
SUPABASE_KEY = "sb_publishable_gBj-IUXwTe8E1olKTLRBhg_l87QRjXu"

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)
supabase = get_supabase()

st.set_page_config(page_title="KING SLESHA MOZ V8", page_icon="👑", layout="centered")
st.markdown("""<div style="text-align:center;background:black;padding:20px;border-radius:15px;border:2px solid #1DB954;">
<h1 style="color:#1DB954;">👑 KING SLESHA MOZ V8</h1><p style="color:white;">✅ BANCO QUE NUNCA APAGA - SUPABASE OK</p></div>""", unsafe_allow_html=True)

def salvar_musica(titulo, artista, tel, status="pendente"):
    isrc = f"MZ-{''.join(random.choices(string.ascii_uppercase, k=3))}-{datetime.datetime.now().year}-{''.join(random.choices(string.digits, k=5))}"
    upc = ''.join(random.choices(string.digits, k=12))
    data = {"titulo": titulo, "artista": artista, "tel": tel, "status": status, "data_envio": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), "isrc": isrc, "upc": upc}
    supabase.table("musicas").insert(data).execute()
    return isrc, upc

def listar_musicas():
    try:
        res = supabase.table("musicas").select("*").order("created_at", desc=True).execute()
        return res.data
    except: return []

menu = st.selectbox("Navegação", ["🏠 Catálogo Spotify", "🚀 Lançar no Spotify AUTO", "🔐 Painel Spotify Provider"])

if menu == "🏠 Catálogo Spotify":
    st.subheader("🟢 No Spotify via King Slesha Moz")
    musicas = listar_musicas()
    aprovadas = [m for m in musicas if m.get('status') == 'aprovada']
    if not aprovadas: st.info("Nenhuma música no Spotify ainda. Lança a primeira!")
    else:
        for m in aprovadas: st.success(f"🎵 {m['titulo']} - {m['artista']} | ISRC: {m['isrc']}")

elif menu == "🚀 Lançar no Spotify AUTO":
    st.subheader("🚀 Enviar música pro Spotify")
    titulo = st.text_input("Título")
    artista = st.text_input("Artista")
    tel = st.text_input("Teu WhatsApp")
    f = st.file_uploader("Música MP3/WAV", type=['mp3','wav'])
    capa = st.file_uploader("Capa 3000x3000", type=['jpg','jpeg','png'])
    if st.button("ENVIAR PARA ANÁLISE 👑"):
        if titulo and artista and tel and f:
            isrc, upc = salvar_musica(titulo, artista, tel, "pendente")
            st.success(f"Recebido! ISRC: {isrc} | UPC: {upc}")
            st.balloons()
            st.info("Vai no Painel senha king2024 pra aprovar!")
        else: st.warning("Preenche tudo!")

elif menu == "🔐 Painel Spotify Provider":
    senha = st.text_input("Senha Provider", type="password")
    if senha == "king2024":
        st.success("✅ ACESSO V8 SUPABASE")
        musicas = listar_musicas()
        st.metric("Na fila", len([m for m in musicas if m['status']=='pendente']))
        st.metric("No Spotify", len([m for m in musicas if m['status']=='aprovada']))
        for m in musicas:
            if m['status'] == 'pendente':
                st.write(f"--- 🎵 **{m['titulo']}** - {m['artista']} | {m['tel']} | ISRC: {m['isrc']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ APROVAR {m['id']}", key=f"ap{m['id']}"):
                        supabase.table("musicas").update({"status":"aprovada"}).eq("id", m['id']).execute()
                        st.rerun()
                with col2:
                    if st.button(f"❌ REJEITAR {m['id']}", key=f"rj{m['id']}"):
                        supabase.table("musicas").delete().eq("id", m['id']).execute()
                        st.rerun()
    elif senha: st.error("Senha errada!")
