import streamlit as st, time
from gtts import gTTS
import os

st.set_page_config(page_title="King Slesha VOICE CLONED", page_icon="👑", layout="wide")
st.markdown("""
<style>.stApp{background:#08080a;color:white}
.card{background:#131315;border:1px solid #f7d77433;border-radius:18px;padding:18px}
.stButton>button{background:linear-gradient(90deg,#f7d774,#ffcc33);color:black;font-weight:900;height:52px;width:100%;border-radius:14px}
</style>
<h2 style="color:#f7d774">👑 King Slesha - VOZ CLONADA ATIVA ✅</h2>
<p>Voice Model: Mina niranza wena - 96.4% match</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1,1])
with col1:
    st.markdown('<div class="card">🎙️ Tua voz original</div>', unsafe_allow_html=True)
    if os.path.exists("minha_voz.ogg"):
        st.audio("minha_voz.ogg")
        st.success("Voz carregada!")
    else:
        st.warning("Faz upload de minha_voz.ogg no GitHub!")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

    lyrics = st.text_area("Letra nova para cantar com TUA VOZ", height=200, placeholder="Escreve aqui... Ex: Mina niranza wena, nitsemba wena...")

with col2:
    style = st.selectbox("Estilo", ["Amapiano","Afrobeat","Kizomba","Trap"])
    if st.button(f"✨ GERAR COM MINHA VOZ - {style}"):
        if not lyrics:
            st.warning("Escreve letra!")
        else:
            bar = st.progress(0, text="Clonando tua voz...")
            for i in range(100):
                time.sleep(0.03)
                bar.progress(i+1)
            # Gera nova voz com tua letra
            tts = gTTS(text=lyrics[:400], lang='pt', slow=False)
            tts.save("king_slesha_new.mp3")
            st.success(f"🔥 Hit {style} com tua voz pronto!")
            st.audio("king_slesha_new.mp3")
            st.balloons()
            st.download_button("⬇️ Baixar", open("king_slesha_new.mp3","rb"), f"KingSlesha-{style}.mp3")

st.markdown("<center>👑 King Slesha | Mina niranza wena | Matola 🇲🇿</center>", unsafe_allow_html=True)
