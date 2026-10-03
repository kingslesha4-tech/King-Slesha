import streamlit as st
st.set_page_config(page_title="King Slesha FREE NO TOKEN", page_icon="👑")
st.markdown("### 👑 King Slesha - SEM TOKEN, SEM MÁFIA")

prompt = st.text_input("Beat", "Amapiano log drum romantic Mozambique 90 BPM")
dur = st.slider("Segundos", 5, 15, 8)

if st.button("🔥 GERAR GRÁTIS SEM TOKEN"):
    try:
        from gradio_client import Client
        with st.spinner("Gerando... 40s"):
            client = Client("facebook/MusicGen", verbose=False)
            audio = client.predict(prompt, dur, fn_index=0)
            st.success("✅ BEAT REAL GERADO!")
            st.audio(audio)
            st.download_button("⬇️ BAIXAR", open(audio,"rb").read(), "beat.wav")
    except Exception as e:
        st.error(f"Erro: {e}")
        st.markdown("**USA DIRETO AQUI - SEM CÓDIGO:**")
        st.link_button("CLICA AQUI PRA GERAR GRÁTIS (Site Oficial Meta)", "https://huggingface.co/spaces/facebook/MusicGen")

st.markdown("---")
st.caption("Se teu app falhar, clica no botão azul acima - é o site oficial da Meta que gera grátis sem token!")
