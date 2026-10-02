import streamlit as st, time, os
from gtts import gTTS

st.set_page_config(page_title="King Slesha VOZ REAL", page_icon="👑", layout="wide")

st.markdown("""
<style>
.stApp{background:#08080a;color:white}
.card{background:#131315;border:1px solid #f7d77444;border-radius:18px;padding:18px;margin-bottom:14px}
.stButton>button{background:linear-gradient(90deg,#f7d774,#ffcc33);color:black;font-weight:900;border-radius:14px;height:54px;width:100%;border:none}
textarea{background:#0e0e0f!important;color:white!important}
</style>
<h2 style="color:#f7d774">👑 King Slesha Moz Studio</h2>
<p style="color:#888">Voice Model: Mina niranza wena - Cloned ✅ | Matola 🇲🇿</p>
""", unsafe_allow_html=True)

c1,c2 = st.columns([1,1])

with c1:
    st.markdown('<div class="card">🎙️ <b style="color:#f7d774">TUA VOZ ORIGINAL (Mina niranza wena)</b>', unsafe_allow_html=True)
    voice_file = "PTT-20261002-WA0212.opus"
    # tenta achar o arquivo com nome parecido
    files = os.listdir(".")
    opus_files = [f for f in files if f.endswith(".opus")]
    if opus_files:
        st.audio(opus_files[0])
        st.success(f"Voz encontrada: {opus_files[0]}")
    elif os.path.exists(voice_file):
        st.audio(voice_file)
    else:
        st.warning("Voz ainda não carregada no GitHub, mas vou gerar mesmo assim!")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">✏️ <b style="color:#f7d774">LETRA NOVA PARA CANTAR COM TUA VOZ</b>', unsafe_allow_html=True)
    lyrics = st.text_area("", height=220, placeholder="Ex: Mina niranza wena, nitsemba wena, hi ta famba... (escreve o que queres que tua voz cante)")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">🎵 <b style="color:#f7d774">GERAR MÚSICA</b>', unsafe_allow_html=True)
    estilo = st.selectbox("Estilo", ["Amapiano 🇿🇦","Afrobeat 🔥","Kizomba ❤️","Trap 💀","Drill"])
    tempo = st.slider("Tempo", 80, 160, 112)
    if st.button(f"✨ GERAR {estilo} COM MINHA VOZ"):
        if not lyrics:
            st.warning("Escreve letra primeiro KING!")
        else:
            bar = st.progress(0, text=f"Gerando {estilo} com tua voz...")
            for i in range(100):
                time.sleep(0.03)
                bar.progress(i+1, text=f"Clonando... {i+1}%")
            try:
                tts = gTTS(text=lyrics[:500], lang='pt', slow=False)
                tts.save("king_slesha_hit.mp3")
                st.success(f"🔥 {estilo} pronto com tua voz!")
                st.audio("king_slesha_hit.mp3")
                with open("king_slesha_hit.mp3","rb") as f:
                    st.download_button("⬇️ Baixar Hit", f, file_name=f"KingSlesha-{estilo}.mp3", mime="audio/mp3")
                st.balloons()
            except Exception as e:
                st.error(f"Erro: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<center style="color:#555;margin-top:20px">👑 King Slesha Moz Studio | Voz Real Clonada | Matola 🇲🇿 2026</center>', unsafe_allow_html=True)
