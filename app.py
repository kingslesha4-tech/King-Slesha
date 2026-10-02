import streamlit as st, time, requests, os
from gtts import gTTS
from pydub import AudioSegment

st.set_page_config(page_title="King Slesha MIX AUTO", page_icon="👑", layout="wide")
st.markdown("""
<style>
.stApp{background:#08080a;color:white}
.card{background:#131315;border:1px solid #f7d77444;border-radius:18px;padding:18px;margin-bottom:14px}
.stButton>button{background:linear-gradient(90deg,#f7d774,#ffcc33);color:black;font-weight:900;height:56px;width:100%;border-radius:14px;border:none}
</style>
<h2 style="color:#f7d774">👑 King Slesha - MIX AUTO v5.0</h2>
<p style="color:#888">Voz + Beat Misturados Juntos Automático ✅</p>
""", unsafe_allow_html=True)

c1,c2 = st.columns([1,1])
with c1:
    st.markdown('<div class="card">✏️ <b style="color:#f7d774">LETRA</b>', unsafe_allow_html=True)
    title = st.text_input("Título", "Mina niranza wena")
    lyrics = st.text_area("Letra", height=200, value="Mina niranza wena nitsemba wena hi ta famba na wena matimba ya mina King Slesha de Matola Mozambique no coração")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">🎵 <b style="color:#f7d774">GERAR MÚSICA MIXADA</b>', unsafe_allow_html=True)
    estilo = st.selectbox("Beat", ["Amapiano 🇿🇦 112 BPM","Kizomba ❤️ 90 BPM","Afrobeat 🔥 110 BPM"])

    beats = {
        "Amapiano 🇿🇦 112 BPM": "https://cdn.pixabay.com/download/audio/2022/03/24/audio_9c8c417d9b.mp3",
        "Kizomba ❤️ 90 BPM": "https://cdn.pixabay.com/download/audio/2021/11/09/audio_884fe212ff.mp3",
        "Afrobeat 🔥 110 BPM": "https://cdn.pixabay.com/download/audio/2022/06/07/audio_b9bd4170e8.mp3"
    }

    vol_beat = st.slider("Volume do Beat", 0, 100, 35)
    vol_voz = st.slider("Volume da Voz", 0, 100, 90)

    if st.button(f"🔥 GERAR MIX {estilo.split(' ')[0]} - VOZ + BEAT JUNTOS"):
        bar = st.progress(0, text="Baixando beat...")
        try:
            # 1. Baixa beat
            r = requests.get(beats[estilo], timeout=20)
            open("beat.mp3","wb").write(r.content)
            bar.progress(30, text="Gerando voz...")

            # 2. Gera voz
            tts = gTTS(text=lyrics[:600], lang='pt', slow=False)
            tts.save("voz.mp3")
            bar.progress(60, text="Misturando voz + beat...")

            # 3. MIXA AUTOMÁTICO
            beat = AudioSegment.from_mp3("beat.mp3")
            voz = AudioSegment.from_mp3("voz.mp3")

            # Corta beat do tamanho da voz + 2s
            beat = beat[:len(voz)+2000]

            # Ajusta volumes
            beat = beat - (100 - vol_beat) # diminui volume
            voz = voz - (100 - vol_voz) + 5

            # Mistura
            mixed = beat.overlay(voz, position=500) # voz começa depois de 0.5s
            mixed.export("king_slesha_mix.mp3", format="mp3")

            bar.progress(100, text="Pronto!")
            st.success(f"🔥 MIX PRONTO! Voz cantando EM CIMA do beat {estilo}!")

            st.markdown("### 🎧 TOCA AQUI - VOZ + BEAT JUNTOS:")
            st.audio("king_slesha_mix.mp3")

            st.markdown("---")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("Voz separada:")
                st.audio("voz.mp3")
            with col_b:
                st.markdown("Beat separado:")
                st.audio("beat.mp3")

            with open("king_slesha_mix.mp3","rb") as f:
                st.download_button("⬇️ BAIXAR MÚSICA MIXADA", f, f"{title}-MIX.mp3", mime="audio/mp3")

            st.balloons()

        except Exception as e:
            st.error(f"Erro no mix: {e}")
            st.info("Se der erro de ffmpeg, avisa que eu faço versão sem pydub!")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<center style="color:#555">👑 King Slesha v5.0 MIX AUTO | Matola 🇲🇿 | Voz + Beat Juntos</center>', unsafe_allow_html=True)
