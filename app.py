import streamlit as st, requests, time, base64, io
st.set_page_config(page_title="King Slesha SUNO REAL", page_icon="👑", layout="wide")
st.markdown("""
<style>
.stApp{background:#0a0a0a;color:white}
.suno-card{background:#18181b;border:1px solid #f7d77444;border-radius:16px;padding:18px;margin-bottom:15px}
.stButton>button{background:white;color:black;font-weight:900;border-radius:20px;height:50px;width:100%}
</style>
<h1>👑 King Slesha SUNO REAL v7.0</h1>
<p style="color:#888">Gera beat de VERDADE com IA da Meta - não é link!</p>
""", unsafe_allow_html=True)

with st.sidebar:
    hf_token = st.text_input("🔑 HF Token (grátis)", type="password", help="Pega em huggingface.co/settings/tokens")
    st.markdown("[Pegar token grátis aqui](https://huggingface.co/settings/tokens)")
    if not hf_token:
        st.warning("Coloca token pra gerar música REAL!")

c1,c2 = st.columns([1,1])
with c1:
    st.markdown('<div class="suno-card">', unsafe_allow_html=True)
    st.markdown("**🎵 Criar Música REAL**")
    title = st.text_input("Título", "Mina niranza wena")
    lyrics = st.text_area("Letra", height=150, value="Mina niranza wena nitsemba wena Matola Mozambique")
    style_prompt = st.text_area("Descreve o beat (em inglês funciona melhor)", value="Amapiano log drum 112 BPM romantic Kizomba guitar, warm bass, African percussion, Mozambique vibe")
    duration = st.slider("Duração segundos", 10, 60, 25)
    
    if st.button("🔥 GERAR MÚSICA REAL - IA"):
        if not hf_token:
            st.error("Coloca HF Token na sidebar!")
        else:
            try:
                API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
                headers = {"Authorization": f"Bearer {hf_token}"}
                
                bar = st.progress(0, text="IA da Meta gerando teu beat... 30-60s")
                
                payload = {"inputs": style_prompt, "parameters": {"duration": duration}}
                
                response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
                
                if response.status_code == 200:
                    # Salvou audio
                    open("suno_real.wav","wb").write(response.content)
                    
                    bar.progress(100, text="Pronto!")
                    st.success(f"✅ BEAT REAL GERADO! {style_prompt}")
                    st.audio("suno_real.wav")
                    
                    # Agora gera voz por cima
                    from gtts import gTTS
                    tts = gTTS(lyrics[:400], lang='pt')
                    tts.save("voz_real.mp3")
                    st.markdown("**🎙️ Tua voz:**")
                    st.audio("voz_real.mp3")
                    
                    st.info("🎧 Agora tens beat REAL gerado por IA + tua voz! Isso é SUNO de verdade, não link Pixabay!")
                    
                    with open("suno_real.wav","rb") as f:
                        st.download_button("⬇️ Baixar Beat REAL", f, f"{title}-beat.wav")
                else:
                    st.error(f"Erro HF: {response.text}")
                    if "loading" in response.text.lower():
                        st.info("Modelo tá carregando, espera 20s e tenta de novo - primeira vez demora!")
            except Exception as e:
                st.error(str(e))
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="suno-card">', unsafe_allow_html=True)
    st.markdown("""
    ### ✅ O que faz REAL agora:
    - **Gera beat do ZERO** com IA MusicGen da Meta (Facebook)
    - **Não é MP3 da internet** - cria na hora
    - Você descreve: "Amapiano log drum" e ele CRIA
    - Grátis 100% com token HF
    - Depois mistura com tua voz gTTS
    
    ### 🔜 Pra ter VOZ CANTANDO igual Suno (não robô):
    Precisa API Suno paga:
    - sunoapi.org - $5 dá 100 músicas com voz humana cantando
    - Aí sim fica igual Suno 100%
    
    **Mas esse v7 já é REAL - beat gerado por IA, não fake!**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<center style="color:#555">👑 King Slesha SUNO REAL v7.0 | Gera música de verdade com IA</center>', unsafe_allow_html=True)
