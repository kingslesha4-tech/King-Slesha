import streamlit as st

st.set_page_config(page_title="King Slesha Moz IA", page_icon="👑")

st.title("👑 King Slesha Moz - Gaza Amapiano AI")
st.subheader("De Matola pro Mundo - Gaza no topo! 🇲🇿")

nome = st.text_input("Teu nome artístico:", "King Slesha")
tema = st.selectbox("Tema:", ["Gaza Life", "Amapiano Duro", "Love Gaza", "Rua / Struggle", "Flex / Dinheiro"])
vibe = st.slider("Vibe Gaza:", 0, 100, 90)

if st.button("🔥 GERAR HIT GAZA"):
    st.success(f"""
    **HIT GAZA PARA {nome.upper()}**

    [Intro]
    Ey, Gaza! De Matola pro mundo!

    [Verso 1]
    Tema {tema}, vida real na zona
    Amapiano batendo, vibe {vibe}%
    Gaza no topo, ninguém nos pressiona

    [Refrão]
    Gaza, Gaza no topo! (x4)

    [Prompt Video]
    Mozambican Amapiano artist {nome}, Gaza style, Maputo, 4k video
    """)
    st.balloons()

st.markdown("---")
st.caption("Feito por King Slesha Moz - 2026")
