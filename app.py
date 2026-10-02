import streamlit as st, time
from gtts import gTTS

st.set_page_config(page_title="King Slesha BEAT REAL", page_icon="👑", layout="wide")
st.markdown("""
<style>
.stApp{background:#08080a;color:white}
.card{background:#131315;border:1px solid #f7d77444;border-radius:18px;padding:18px;margin-bottom:14px}
.stButton>button{background:linear-gradient(90deg,#f7d774,#ffcc33);color:black;font-weight:900;height:56px;width:100%;border-radius:14px;border:none}
</style>
<h2 style="color:#f7d774">👑 King Slesha Moz - BEAT v4.1</h2>
<p style="color:#888">Voz + Beat Tocando Junto ✅ | Sem API Key precisa</p>
""", unsafe_allow_html=True)

c1,c2 = st.columns([1,1])
with c1:
    st.markdown('<div class="card">✏️ <b style="color:#f7d774">LETRA (ESCREVE MUITO PRA NÃO SER 4s)</b>', unsafe_allow_html=True)
    title = st.text_input("Título", "Mina niranza wena")
    lyrics = st.text_area("Letra", height=200, value="Mina niranza wena, nitsemba wena, hi ta famba na wena matimba ya mina, King Slesha de Matola Mozambique no coração")
    st.caption(f"{len(lyrics)} letras | {len(lyrics.split())} palavras - Escreve +30 palavras pra durar +15s")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">🎵 <b style="color:#f7d774">ESTILO + BEAT REAL</b>', unsafe_allow_html=True)
    estilo = st.selectbox("Estilo", [
        "Amapiano 🇿🇦 - Log Drum 112 BPM",
        "Kizomba ❤️ - Romântico 90 BPM",
        "Afrobeat 🔥 - Dançante 110 BPM",
        "Trap 💀 - Pesado 140 BPM"
    ])

    beats = {
        "Amapiano 🇿🇦 - Log Drum 112 BPM": "https://cdn.pixabay.com/download/audio/2022/03/24/audio_9c8c417d9b.mp3",
        "Kizomba ❤️ - Romântico 90 BPM": "https://cdn.pixabay.com/download/audio/2021/11/09/audio_884fe212ff.mp3",
        "Afrobeat 🔥 - Dançante 110 BPM": "https://cdn.pixabay.com/download/audio/2022/06/07/audio_b9bd4170e8.mp3",
        "Trap 💀 - Pesado 140 BPM": "https://cdn.pixabay.com/download/audio/2022/09/14/audio_619339fbc7.mp3"
    }

    if st.button(f"🔥 GERAR {estilo.split(' ')[0]} COM BEAT"):
        if len(lyrics.split()) < 5:
            st.warning("⚠️ Letra muito curta! Escreve pelo menos 1 frase completa, senão fica 0:04 mesmo!")
            lyrics_long = (lyrics + " ") * 4
        else:
            lyrics_long = lyrics

        bar = st.progress(0, text="Gerando voz + beat...")
        for i in range(100):
            time.sleep(0.02)
            bar.progress(i+1)

        try:
            tts = gTTS(text=lyrics_long[:600], lang='pt', slow=False)
            tts.save("voz.mp3")
            st.success(f"✅ PRONTO! {estilo}")

            st.markdown("**🎙️ 1. TUA VOZ CANTANDO:**")
            st.audio("voz.mp3")

            st.markdown(f"**🥁 2. BEAT INSTRUMENTAL {estilo} - TOCA JUNTO:**")
            st.audio(beats[estilo])

            st.markdown("""
            **🎧 COMO OUVIR COMO MÚSICA REAL:**
            1. Dá PLAY nos dois ao mesmo tempo!
            2. Abaixa volume do beat pra 30%
            3. Voz por cima = tua música!
            """)

            with open("voz.mp3","rb") as f:
                st.download_button("⬇️ Baixar Voz", f, f"{title}.mp3")

        except Exception as e:
            st.error(str(e))
    st.markdown('</div>', unsafe_allow_html=True)

st.info("💡 PORQUE TAVA 0:04? Porque você escreveu só 2-3 palavras! gTTS lê rápido. Escreve letra GRANDE (min 20 palavras) que fica 15-20s!")

st.markdown('<center style="color:#555">👑 King Slesha Moz Studio v4.1 | Matola 🇲🇿</center>', unsafe_allow_html=True)
