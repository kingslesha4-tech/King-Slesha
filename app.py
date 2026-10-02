import streamlit as st, time

st.set_page_config(page_title="King Slesha Moz Studio", page_icon="👑", layout="wide")

st.markdown("""
<style>
.stApp{background:#08080a;color:white}
.card{background:#131315;border:1px solid #f7d77433;border-radius:18px;padding:18px;margin-bottom:16px}
.topbar{display:flex;justify-content:space-between;align-items:center;background:#131315;border:1px solid #f7d77433;border-radius:16px;padding:12px 18px}
.logo{color:#f7d774;font-weight:900;line-height:1.1}
.badge{background:#f7d774;color:black;border-radius:20px;padding:5px 12px;font-size:12px;font-weight:800}
.stButton>button{background:linear-gradient(90deg,#f7d774,#ffcc33);color:black;font-weight:900;border-radius:14px;height:52px;width:100%;border:none}
textarea{background:#0e0e0f!important;color:white!important}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
<div style="display:flex;gap:10px;align-items:center"><span style="font-size:26px">👑</span><div class="logo">King Slesha Moz<br>Music Studio</div></div>
<div style="display:flex;gap:14px;color:#888"><b style="color:#f7d774;border-bottom:2px solid #f7d774">Create</b><span>Library</span><span>Projects</span><span>Sounds</span></div>
<div>🔔 ⚙️ <span style="background:#f7d774;color:black;border-radius:50%;padding:4px 10px">A</span></div>
</div>
<div style="text-align:right;margin-top:8px"><span class="badge">Model: KingSlesha-Music v2.1</span></div>
""", unsafe_allow_html=True)

st.markdown("## Create New Track")
st.caption("Generate original music with AI — lyrics, style, and voice in seconds")

c1,c2 = st.columns([1.2,0.8])
with c1:
    st.markdown('<div class="card">✏️ <b style="color:#f7d774">LYRICS INPUT</b>', unsafe_allow_html=True)
    lyrics=st.text_area("", height=280, placeholder="[Verse]\nIn the night we rise, yeah, the city glow,\nMozambique heart beating loud and bold...\n[Chorus]\nKing Slesha, we shining bright...")
    st.caption(f"{len(lyrics)}/1000 characters • Tip: Use [Chorus], [Verse]")
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="card">🎵 <b style="color:#f7d774">INSTRUMENTAL STYLE</b>', unsafe_allow_html=True)
    style=st.selectbox("Style", ["Amapiano 🇿🇦","Afrobeat 🔥","Trap 💀","Drill","Kizomba ❤️"])
    st.markdown('<b style="color:#f7d774">VOICE SELECTOR</b>', unsafe_allow_html=True)
    voice=st.selectbox("", ["Male • Calm & Soulful","Mali — Warm & Smooth","King Slesha Original"])
    colA,colB=st.columns(2)
    colA.slider("Tempo",80,160,112)
    colB.slider("Duration",30,180,150)
    if st.button("✨ GENERATE"):
        if not lyrics: st.warning("Escreve letra KING!")
        else:
            bar=st.progress(0,text=f"Gerando {style}...")
            for i in range(100): time.sleep(0.02); bar.progress(i+1)
            st.success(f"🔥 Hit {style} pronto!")
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="card">🎵 <b>Untitled Track • Ready to Generate</b> <span style="float:right">⏮️ ▶️ ⏭️ 🔊</span></div><center style="color:#555">👑 King Slesha Moz Studio | Matola 🇲🇿</center>', unsafe_allow_html=True)
