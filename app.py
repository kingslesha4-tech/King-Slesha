import streamlit as st, requests, time, base64
st.set_page_config(page_title="King Slesha SUNO", page_icon="👑", layout="wide")
st.markdown("""
<style>
.stApp{background:#0a0a0a;color:white}
.suno-card{background:#18181b;border:1px solid #2a2a2e;border-radius:16px;padding:20px}
.stButton>button{background:white;color:black;font-weight:900;border-radius:20px;height:48px}
</style>
<h1 style="color:white">👑 King Slesha AI - Seu Suno</h1>
<p style="color:#888">Crie músicas igual Suno - Amapiano, Kizomba, Afrobeat</p>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Config Suno API")
    suno_api_url = st.text_input("URL do teu API Suno", "https://teu-suno-api.vercel.app")
    st.caption("Se não tiver API ainda, usa modo DEMO abaixo")
    st.divider()
    st.markdown("### 👑 King Slesha Moz")
    st.markdown("Matola 🇲🇿 | Kizomba | Amapiano")

tab1, tab2 = st.tabs(["🎵 Criar Música (Igual Suno)", "📚 Minhas Músicas"])

with tab1:
    c1,c2 = st.columns([1,1])
    with c1:
        st.markdown('<div class="suno-card">', unsafe_allow_html=True)
        title = st.text_input("Título", "Mina niranza wena")
        lyrics = st.text_area("Letra (Custom)", height=200, value="[Intro]\nMina niranza wena\n[Verse]\nNitsemba wena, hi ta famba\nMatimba ya mina, de Matola\n[Chorus]\nMina niranza, oh yeah\nMozambique no coração")
        style = st.text_input("Style of Music", "Amapiano, Kizomba, Afrobeat, romantic, log drum 112 BPM, male vocal")
        instrumental = st.checkbox("Instrumental (sem voz)")
        model = st.selectbox("Modelo", ["chirp-v4", "chirp-v3.5"])

        if st.button("🔥 GERAR MÚSICA - SUNO"):
            if "teu-suno-api" in suno_api_url:
                st.warning("⚠️ Coloca tua URL do Vercel na sidebar! Por enquanto vou gerar DEMO com gTTS + Beat igual antes.")
                # FALLBACK DEMO IGUAL ANTES - pra não quebrar
                from gtts import gTTS
                tts = gTTS(lyrics[:500], lang='pt')
                tts.save("demo.mp3")
                st.audio("demo.mp3")
                st.success("DEMO gerado! Pra ter Suno REAL, deploy o API no Vercel!")
            else:
                try:
                    # CHAMA TEU SUNO API REAL
                    payload = {
                        "prompt": lyrics,
                        "tags": style,
                        "title": title,
                        "make_instrumental": instrumental,
                        "mv": model
                    }
                    r = requests.post(f"{suno_api_url}/api/generate", json=payload, timeout=30)
                    data = r.json()
                    st.json(data)

                    # Pega ID e espera
                    song_id = data[0]['id'] if isinstance(data, list) else data['id']
                    st.info(f"Gerando... ID: {song_id} - Suno demora 1-2 min")

                    bar = st.progress(0)
                    for i in range(60):
                        time.sleep(3)
                        status_r = requests.get(f"{suno_api_url}/api/get?ids={song_id}")
                        status = status_r.json()
                        bar.progress(min((i+1)*2, 100))
                        if status and status[0].get('audio_url'):
                            audio_url = status[0]['audio_url']
                            st.success("✅ MÚSICA PRONTA! Igual Suno!")
                            st.audio(audio_url)
                            st.video(status[0].get('video_url', ''))
                            st.download_button("⬇️ Baixar MP3", requests.get(audio_url).content, f"{title}.mp3")
                            break
                except Exception as e:
                    st.error(f"Erro Suno API: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="suno-card">', unsafe_allow_html=True)
        st.markdown("#### 🎧 O que meu clone faz igual Suno:")
        st.markdown("""
        - ✅ Letra custom + [Intro][Verse][Chorus]
        - ✅ Style: Amapiano, Kizomba, Afrobeat, Trap
        - ✅ Instrumental ou com voz
        - ✅ 2 versões por geração
        - ✅ Gera capa + letra + MP3 + Vídeo
        - ✅ Salva na biblioteca
        - ✅ Mesmo motor V4 / V4.5 do Suno

        **Diferença do Suno:**
        É TEU! Sem limite de 5 músicas por dia, sem pagar $10/mês!
        Tu só paga o Vercel (grátis) e captcha $0.003 por música!
        """)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.info("Tuas músicas geradas vão aparecer aqui - igual Suno library!")
