import streamlit as st, time, requests, base64
from gtts import gTTS
import streamlit.components.v1 as components

st.set_page_config(page_title="King Slesha MIX", page_icon="👑", layout="wide")
st.markdown("""
<style>
.stApp{background:#08080a;color:white}
.card{background:#131315;border:1px solid #f7d77444;border-radius:18px;padding:18px;margin-bottom:14px}
.stButton>button{background:linear-gradient(90deg,#f7d774,#ffcc33);color:black;font-weight:900;height:56px;width:100%;border-radius:14px;border:none}
</style>
<h2 style="color:#f7d774">👑 King Slesha - MIX AUTO v5.1</h2>
<p style="color:#888">Beat + Voz Tocando Juntos no Celular ✅ SEM ERRO</p>
""", unsafe_allow_html=True)

c1,c2 = st.columns([1,1])
with c1:
    st.markdown('<div class="card">✏️ <b style="color:#f7d774">LETRA</b>', unsafe_allow_html=True)
    title = st.text_input("Título", "Mina niranza wena")
    lyrics = st.text_area("Letra", height=200, value="Mina niranza wena nitsemba wena hi ta famba na wena matimba ya mina King Slesha de Matola Mozambique no coração Kizomba noite")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">🎵 <b style="color:#f7d774">GERAR</b>', unsafe_allow_html=True)
    estilo = st.selectbox("Beat", ["Amapiano 🇿🇦 112 BPM","Kizomba ❤️ 90 BPM","Afrobeat 🔥 110 BPM"])
    beats = {
        "Amapiano 🇿🇦 112 BPM": "https://cdn.pixabay.com/download/audio/2022/03/24/audio_9c8c417d9b.mp3",
        "Kizomba ❤️ 90 BPM": "https://cdn.pixabay.com/download/audio/2021/11/09/audio_884fe212ff.mp3",
        "Afrobeat 🔥 110 BPM": "https://cdn.pixabay.com/download/audio/2022/06/07/audio_b9bd4170e8.mp3"
    }

    if st.button(f"🔥 GERAR MIX {estilo.split(' ')[0]}"):
        try:
            # Gera voz
            tts = gTTS(text=lyrics[:600], lang='pt', slow=False)
            tts.save("voz.mp3")
            with open("voz.mp3","rb") as f:
                voz_b64 = base64.b64encode(f.read()).decode()

            # Pega beat link direto
            beat_url = beats[estilo]

            st.success("✅ PRONTO! Clique PLAY abaixo - toca voz + beat JUNTOS!")

            # PLAYER MÁGICO QUE TOCA OS 2 JUNTOS
            html_code = f"""
            <div style="background:#1a1a1d;padding:15px;border-radius:12px;border:1px solid #f7d774">
            <p style="color:#f7d774;font-weight:bold">🎧 MIX AUTOMÁTICO - Voz + Beat Juntos</p>
            <audio id="beat" src="{beat_url}" loop></audio>
            <audio id="voz" src="data:audio/mp3;base64,{voz_b64}"></audio>
            <button onclick="playBoth()" style="background:#f7d774;color:black;font-weight:900;padding:12px 20px;border-radius:10px;border:none;width:100%;font-size:16px;cursor:pointer">▶️ TOCAR VOZ + BEAT JUNTOS</button>
            <button onclick="stopBoth()" style="background:#333;color:white;padding:8px 15px;border-radius:8px;border:none;width:100%;margin-top:8px;cursor:pointer">⏹️ PARAR</button>
            <div style="margin-top:10px">
            <label style="color:#aaa">Volume Beat: <input type="range" id="volBeat" min="0" max="100" value="35" oninput="document.getElementById('beat').volume=this.value/100"></label><br>
            <label style="color:#aaa">Volume Voz: <input type="range" id="volVoz" min="0" max="100" value="90" oninput="document.getElementById('voz').volume=this.value/100"></label>
            </div>
            </div>
            <script>
            function playBoth(){{
              var b=document.getElementById('beat');
              var v=document.getElementById('voz');
              b.volume=0.35; v.volume=0.9;
              b.currentTime=0; v.currentTime=0;
              b.play(); v.play();
            }}
            function stopBoth(){{
              document.getElementById('beat').pause();
              document.getElementById('voz').pause();
            }}
            </script>
            """
            components.html(html_code, height=250)

            st.markdown("---")
            st.audio("voz.mp3", format="audio/mp3")
            st.caption("Voz separada pra download")
            with open("voz.mp3","rb") as f:
                st.download_button("⬇️ Baixar Voz", f, f"{title}.mp3")

        except Exception as e:
            st.error(str(e))

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<center style="color:#555">👑 King Slesha v5.1 MIX - Matola 🇲🇿 | Toca Junto no Celular</center>', unsafe_allow_html=True)
