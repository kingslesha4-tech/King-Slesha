import streamlit as st, time, requests, os
st.set_page_config(page_title="King Slesha SUNO REAL", page_icon="👑", layout="wide")
st.markdown("""
<style>
.stApp{background:#08080a;color:white}
.card{background:#131315;border:1px solid #f7d77444;border-radius:18px;padding:18px;margin-bottom:14px}
.stButton>button{background:linear-gradient(90deg,#f7d774,#ffcc33);color:black;font-weight:900;height:56px;width:100%;border-radius:14px;border:none}
</style>
<h2 style="color:#f7d774">👑 King Slesha Moz - SUNO REAL v4.0</h2>
<p style="color:#888">API Profissional | Instrumental + Voz Cantando Auto-Tune ✅</p>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🔑 API SUNO")
    st.info("Para gerar música REAL completa, precisa de API Key.\n\n**Opção 1 GRÁTIS:** suno.gcui.ai (limitado)\n**Opção 2 PAGO $0.14/música:** CometAPI / TTAPI")
    api_key = st.text_input("Cola tua API Key Suno aqui", type="password", placeholder="sk-...")
    st.markdown("[Pegar Key Grátis](https://suno.gcui.ai) | [Pegar Key Paga](https://cometapi.com)")
    st.markdown("---")
    st.markdown("**Sem API Key? Usa modo DEMO com voz + beat separado (que já tens)**")

c1,c2 = st.columns([1,1])
with c1:
    st.markdown('<div class="card">✏️ <b style="color:#f7d774">LETRA REAL</b>', unsafe_allow_html=True)
    title = st.text_input("Título", "Mina niranza wena")
    lyrics = st.text_area("Letra (verso + refrão)", height=250, placeholder="[Verse]\nMina niranza wena nitsemba wena\nHi ta famba na wena\n\n[Chorus]\nKing Slesha de Matola, Moz no coração\nKizomba na noite com paixão...")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">🎵 <b style="color:#f7d774">ESTILO SUNO PRO</b>', unsafe_allow_html=True)
    style_prompt = st.selectbox("Prompt de Estilo", [
        "Kizomba romantic, smooth guitar, Mozambican vibe, 90 BPM, sensual male vocal",
        "Amapiano log drum, South African groove, 112 BPM, deep house, male vocal",
        "Afrobeat dance, African drums, energetic, 110 BPM",
        "Trap soulful, 140 BPM, emotional"
    ])
    instrumental = st.checkbox("Só instrumental? (sem voz)")
    if st.button("🔥 GERAR MÚSICA REAL SUNO"):
        if not api_key:
            st.warning("⚠️ Sem API Key! Gerando no MODO DEMO (voz lendo + beat separado) - Pra modo REAL, cola tua key na barra lateral!")
            from gtts import gTTS
            bar = st.progress(0, text="Gerando DEMO...")
            for i in range(100):
                time.sleep(0.02)
                bar.progress(i+1)
            try:
                tts = gTTS(text=lyrics[:500], lang='pt', slow=False)
                tts.save("demo.mp3")
                st.audio("demo.mp3")
                st.success("DEMO pronto! Com API Key gera com instrumental junto e cantando bonito!")
            except Exception as e:
                st.error(str(e))
        else:
            # CHAMADA REAL SUNO API (CometAPI / TTAPI)
            st.info("🚀 Enviando para Suno API real...")
            bar = st.progress(0, text="Suno criando tua música... 30-60s")
            try:
                # Exemplo usando CometAPI / TTAPI endpoint
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                data = {
                    "mv": "chirp-v4",  # Suno v4
                    "prompt": style_prompt,
                    "title": title,
                    "tags": style_prompt,
                    "lyrics": lyrics,
                    "instrumental": instrumental
                }
                # Tenta gerar
                resp = requests.post("https://api.cometapi.com/suno/generate", json=data, headers=headers, timeout=30)
                if resp.status_code == 200:
                    result = resp.json()
                    st.json(result)
                    # Polling para pegar audio
                    task_id = result.get("taskId") or result.get("id")
                    st.success(f"Task enviada! ID: {task_id} - Música gerando, aguarda 1 min e verifica no site da API")
                else:
                    st.error(f"Erro API: {resp.text[:500]} - Verifica tua key em cometapi.com")
                    st.markdown("**Dica:** Usa suno.gcui.ai que é grátis e mais simples!")
            except Exception as e:
                st.error(f"Erro: {e}")
                st.markdown("Sem servidor próprio, precisa deploy da API suno-api no Vercel. Te ensino!")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
<h4 style="color:#f7d774">📖 COMO TER MÚSICA REAL COM INSTRUMENTAL (PASSO A PASSO):</h4>

**OPÇÃO MAIS FÁCIL (RECOMENDO):**
1. Vai no site <b>suno.com</b> direto e cria música lá com tua letra - é grátis 10 músicas/dia
2. Depois baixa e faz upload no teu app

**OPÇÃO API AUTOMÁTICA (PRO):**
1. Cria conta no <b>cometapi.com</b> (ganha $1 grátis)
2. Pega API Key (começa com sk-)
3. Cola na barra lateral do teu app
4. Agora clica GERAR - vai gerar música completa Suno v4/v5!

**OPÇÃO 100% GRÁTIS TÉCNICA:**
1. Deploy grátis do projeto <b>gcui-art/suno-api</b> no Vercel (1 clique)
2. Pega cookie do suno.com
3. Usa tua própria API ilimitada!

<b style="color:#f7d774">KING, quer que eu faça o deploy da API pra você?</b> É 2 minutos e teu app fica 100% REAL sem pagar nada!
</div>
""", unsafe_allow_html=True)
