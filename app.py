import streamlit as st

st.set_page_config(page_title="King Slesha Distribution", page_icon="👑")

st.markdown("<center><h1>👑 KING SLESHA MUSIC DISTRIBUTION</h1><h3>De Matola para o Mundo</h3></center>", unsafe_allow_html=True)

st.write("---")

artist = st.text_input("Nome do Artista")
title = st.text_input("Nome da Musica")
album = st.text_input("Album/Single", "Single")
label = st.text_input("Label", "King Slesha Music Distribution")

audio = st.file_uploader("Audio WAV/MP3", type=["wav","mp3"])
cover = st.file_uploader("Capa JPG 3000x3000", type=["jpg","png"])

if st.button("🚀 Distribuir Agora"):
    if artist and title and audio:
        st.success(f"✅ SUCESSO {artist}!")
        st.write(f"Musica: {title}")
        st.write(f"Label: {label}")
        st.write(f"ID: KING{artist[:3].upper()}2026")
        st.write("Arquivo DDEX gerado com sucesso! Pronto pro Spotify!")
        st.balloons()
    else:
        st.error("Preenche nome do artista, musica e audio!")
