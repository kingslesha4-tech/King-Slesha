import streamlit as st, requests, time
st.set_page_config(page_title="King Slesha SUNO REAL", page_icon="👑", layout="wide")
st.markdown("<h1>👑 King Slesha - SUNO REAL 100%</h1><p>Voz humana cantando de verdade - não demo!</p>", unsafe_allow_html=True)

api_key = st.sidebar.text_input("API KEY sunoapi.org", type="password")
st.sidebar.link_button("Pegar API KEY $5", "https://sunoapi.org")

title = st.text_input("Título", "Mina niranza wena")
lyrics = st.text_area("Letra", height=200, value="[Verse] Mina niranza wena nitsemba wena\n[Chorus] Matola Mozambique no coração")
style = st.text_input("Estilo", "Amapiano romantic Kizomba 90 BPM male vocal")

if st.button("🔥 GERAR SUNO REAL - VOZ HUMANA"):
    if not api_key:
        st.error("Coloca API KEY da sunoapi.org na sidebar! Sem isso não funciona real!")
    else:
        headers = {"Authorization": f"Bearer {api_key}"}
        # 1. Gera
        r = requests.post("https://api.sunoapi.org/api/v1/generate", headers=headers, json={
            "prompt": style,
            "lyrics": lyrics,
            "title": title,
            "customMode": True,
            "instrumental": False,
            "model": "V4_5"
        })
        st.json(r.json())
        task_id = r.json()['data']['taskId']
        
        bar = st.progress(0, text="Suno gerando tua música... 1-2 min")
        for i in range(40):
            time.sleep(5)
            status = requests.get(f"https://api.sunoapi.org/api/v1/get?taskId={task_id}", headers=headers).json()
            bar.progress((i+1)*2)
            if status['data']['status'] == 'SUCCESS':
                for track in status['data']['tracks']:
                    st.success("✅ MÚSICA REAL PRONTA! VOZ HUMANA!")
                    st.audio(track['audioUrl'])
                    st.image(track['imageUrl'])
                    st.download_button(f"⬇️ Baixar {track['title']}", requests.get(track['audioUrl']).content, f"{title}.mp3")
                break
