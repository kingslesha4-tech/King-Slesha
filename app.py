import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="King Slesha Distribution", page_icon="👑", layout="wide")

# --- ARQUIVO PARA GUARDAR AS MÚSICAS ---
DB_FILE = "musicas_db.json"
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump([], f)

def load_musicas():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_musicas(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# --- SENHA DO ADMIN (SÓ TU) ---
ADMIN_PASSWORD = "King2026!" # PODES MUDAR ESSA SENHA!

# --- DESIGN ---
st.markdown("""
<style>
    .main { background: #0e1117; }
    .king-header { text-align:center; padding:20px; background: linear-gradient(90deg,#FFD700,#FFA500); border-radius:15px; color:black; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="king-header"><h1>👑 KING-SLESHA MUSIC DISTRIBUTION</h1><p>De Matola para o Mundo</p></div>', unsafe_allow_html=True)

# --- MENU LATERAL ---
menu = st.sidebar.selectbox("MENU", ["🎤 Artista - Enviar Música", "👑 Admin - Aprovação (Só King)", "🌍 Músicas Aprovadas (No Ar)"])

# ============= 1. ARTISTA ENVIA =============
if menu == "🎤 Artista - Enviar Música":
    st.subheader("🎤 Enviar tua música para análise")
    st.info("A tua música vai para o King Slesha analisar. Só ele pode aprovar!")

    with st.form("upload"):
        nome_artista = st.text_input("Nome do Artista")
        titulo = st.text_input("Título da Música")
        genero = st.selectbox("Gênero", ["Amapiano", "Afrobeat", "Hip Hop", "R&B", "Kizomba", "Outro"])
        plataformas = st.multiselect("Distribuir para:", ["Spotify", "Apple Music", "YouTube Music", "Deezer", "TikTok", "Boomplay"], default=["Spotify","Apple Music"])
        audio = st.file_uploader("Arquivo de Áudio (MP3/WAV)", type=["mp3","wav","m4a"])
        capa = st.file_uploader("Capa (JPG/PNG)", type=["jpg","png","jpeg"])
        btn = st.form_submit_button("🚀 ENVIAR PARA O KING APROVAR")

        if btn:
            if not nome_artista or not titulo or not audio:
                st.error("Preenche nome, título e áudio!")
            else:
                musicas = load_musicas()
                nova = {
                    "id": len(musicas)+1,
                    "artista": nome_artista,
                    "titulo": titulo,
                    "genero": genero,
                    "plataformas": plataformas,
                    "data": datetime.now().strftime("%d/%m/%2026 %H:%M"),
                    "status": "PENDENTE", # PENDENTE = esperando tua aprovação
                    "arquivo": audio.name
                }
                musicas.append(nova)
                save_musicas(musicas)
                st.success(f"✅ Enviado! '{titulo}' está PENDENTE. O King Slesha vai analisar!")
                st.balloons()

# ============= 2. ADMIN - SÓ TU APROVA =============
elif menu == "👑 Admin - Aprovação (Só King)":
    st.subheader("👑 ÁREA SECRETA - SÓ O KING ENTRA")
    senha = st.text_input("Digite a senha de Admin:", type="password")
    
    if senha == ADMIN_PASSWORD:
        st.success("Bem-vindo, King Slesha! 👑")
        musicas = load_musicas()
        pendentes = [m for m in musicas if m["status"] == "PENDENTE"]

        if not pendentes:
            st.info("Nenhuma música pendente. Tudo em dia, King!")
        else:
            st.warning(f"Tem {len(pendentes)} músicas para aprovar!")
            for m in pendentes:
                with st.expander(f"🔔 {m['titulo']} - {m['artista']} | {m['genero']}"):
                    st.write(f"**ID:** {m['id']}")
                    st.write(f"**Artista:** {m['artista']}")
                    st.write(f"**Música:** {m['titulo']}")
                    st.write(f"**Plataformas:** {', '.join(m['plataformas'])}")
                    st.write(f"**Enviado em:** {m['data']}")
                    st.write(f"**Arquivo:** {m['arquivo']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"✅ APROVAR {m['id']}", key=f"aprov{m['id']}"):
                            for i in musicas:
                                if i["id"] == m["id"]:
                                    i["status"] = "APROVADO"
                            save_musicas(musicas)
                            st.success(f"{m['titulo']} APROVADO! Agora vai pro Spotify!")
                            st.rerun()
                    with col2:
                        if st.button(f"❌ REJEITAR {m['id']}", key=f"rej{m['id']}"):
                            for i in musicas:
                                if i["id"] == m["id"]:
                                    i["status"] = "REJEITADO"
                            save_musicas(musicas)
                            st.error("Rejeitado!")
                            st.rerun()
    elif senha != "":
        st.error("Senha errada! Sai daqui! 🔒")

# ============= 3. MÚSICAS NO AR =============
else:
    st.subheader("🌍 Músicas que já estão no ar pela King-Slesha")
    musicas = load_musicas()
    aprovadas = [m for m in musicas if m["status"] == "APROVADO"]
    
    if not aprovadas:
        st.info("Ainda nenhuma música aprovada. Seja o primeiro!")
    else:
        for m in aprovadas:
            st.markdown(f"""
            <div style="border:1px solid #FFD700; padding:15px; border-radius:10px; margin:10px 0; background:#1a1a1a;">
            <h3>🎵 {m['titulo']} - {m['artista']}</h3>
            <p>🎧 {m['genero']} | 📅 {m['data']} | ✅ Status: {m['status']}</p>
            <p>🌍 Disponível em: {', '.join(m['plataformas'])}</p>
            </div>
            """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.write("👑 King-Slesha Music © 2026")
st.sidebar.write("📍 Matola, Moçambique")
st.sidebar.write(f"🔑 Senha Admin atual: {ADMIN_PASSWORD}")
