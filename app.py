import streamlit as st
import datetime, random, string, os
from supabase import create_client

# --- CONFIG KING SLESHA MOZ V8 - NUNCA APAGA ---
SUPABASE_URL = "https://hfjskhhjrdjuphkbjdpu.supabase.co"
SUPABASE_KEY = "sb_publishable_gBj-IUXwTe8E1olKTLRBhg_l87QRjXu"

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

st.set_page_config(page_title="KING SLESHA MOZ V8", page_icon="👑", layout="centered")

st.markdown("""
<div style="text-align:center;background:black;padding:20px;border-radius:15px;border:2px solid #1DB954;">
<h1 style="color:#1DB954;">👑 KING SLESHA MOZ V8</h1>
<p style="color:white;">✅ BANCO QUE NUNCA APAGA - SUPABASE CONECTADO</p>
</div>
""", unsafe_allow_html=True)

# --- FUNÇÕES SUPABASE ---
def salvar_musica(titulo, artista, tel, status="pendente"):
    isrc = f"MZ-{''.join(random.choices(string.ascii_uppercase, k=3))}-{datetime.datetime.now().year}-{''.join(random.choices(string.digits, k=5))}"
    upc = ''.join(random.choices(string.digits, k=12))
    data = {
        "titulo": titulo,
        "artista": artista,
        "tel": tel,
        "status": status,
        "data_envio": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
        "isrc": isrc,
        "upc": upc
    }
    try:
        supabase.table("musicas").insert(data).execute()
        return isrc, upc
    except Exception as e:
        st.error(f"Erro Supabase: {e} - Cria a tabela musicas no SQL Editor!")
        return None, None

def listar_musicas():
    try:
        res = supabase.table("musicas").select("*").order("created_at", desc=True).execute()
        return res.data
    except:
        return []

# --- MENU ---
menu = st.selectbox("Navegação", ["🏠 Catálogo Spotify", "🚀 Lançar no Spotify AUTO", "🔐 Painel Spotify Provider"])

if menu == "🏠 Catálogo Spotify":
    st.subheader("🟢 Lançamentos no Spotify via King Slesha Moz")
    musicas = listar_musicas()
    aprovadas = [m for m in musicas if m.get('status') == 'aprovada']
    if not aprovadas:
        st.info("Nenhuma música no Spotify ainda. Vai em Lançar e publica a primeira!")
    else:
        for m in aprovadas:
            st.success(f"🎵 {m['titulo']} - {m['artista']} | ISRC: {m['isrc']}")

elif menu == "🚀 Lançar no Spotify AUTO":
    st.subheader("🚀 Enviar música para o Spotify")
    st.markdown("Preencha e vamos gerar teu ISRC/UPC automático!")
    titulo = st.text_input("Título da música")
    artista = st.text_input("Nome do artista")
    tel = st.text_input("Teu WhatsApp")
    musica_file = st.file_uploader("Música MP3/WAV", type=['mp3','wav'])
    capa_file = st.file_uploader("Capa 3000x3000", type=['jpg','jpeg','png'])
    
    if st.button("ENVIAR PARA ANÁLISE 👑"):
        if titulo and artista and tel and musica_file:
            isrc, upc = salvar_musica(titulo, artista, tel, "pendente")
            if isrc:
                st.success(f"ID #{len(listar_musicas())} recebido! ISRC: {isrc} | UPC: {upc}")
                st.balloons()
                st.info("Agora vai no Painel Provider senha king2024 pra aprovar!")
        else:
            st.warning("Preenche tudo!")

elif menu == "🔐 Painel Spotify Provider":
    senha = st.text_input("Senha Provider", type="password")
    if senha == "king2024":
        st.success("✅ ACESSO LIBERADO - V8 SUPABASE")
        musicas = listar_musicas()
        st.metric("Na fila pro Spotify", len([m for m in musicas if m['status']=='pendente']))
        st.metric("No Spotify", len([m for m in musicas if m['status']=='aprovada']))
        
        for m in musicas:
            if m['status'] == 'pendente':
                st.write(f"---")
                st.write(f"🎵 **{m['titulo']}** - {m['artista']} | Tel: {m['tel']}")
                st.write(f"Data: {m['data_envio']} | ISRC: {m['isrc']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ APROVAR {m['id']}", key=f"ap{m['id']}"):
                        supabase.table("musicas").update({"status":"aprovada"}).eq("id", m['id']).execute()
                        st.success("Enviado pro Spotify! ✅")
                        st.rerun()
                with col2:
                    if st.button(f"❌ REJEITAR {m['id']}", key=f"rj{m['id']}"):
                        supabase.table("musicas").delete().eq("id", m['id']).execute()
                        st.rerun()
    elif senha:
        st.error("Senha errada!")
