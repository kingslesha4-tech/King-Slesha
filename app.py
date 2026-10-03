import streamlit as st, requests
st.set_page_config(page_title="King Slesha FREE", page_icon="👑")
st.markdown("<h1>👑 King Slesha - 100% GRÁTIS SEM MÁFIA</h1>", unsafe_allow_html=True)
st.markdown("Gera música de verdade, sem pagar, sem API KEY!")

prompt = st.text_input("Descreve o beat", "Amapiano log drum romantic Mozambique Kizomba 90 BPM warm bass")
duration = st.slider("Segundos", 5, 30, 15)

if st.button("🔥 GERAR GRÁTIS AGORA - REAL"):
    with st.spinner("IA grátis gerando... 40s (primeira vez demora)"):
        try:
            from gradio_client import Client
            client = Client("facebook/musicgen")
            result = client.predict(
                prompt,
                duration,
                api_name="/predict"
            )
            st.success("✅ BEAT REAL GERADO - GRÁTIS! SEM MÁFIA!")
            st.audio(result)
            st.download_button("⬇️ Baixar", open(result,"rb").read(), "king-slesha-beat.wav")
        except:
            st.info("Tentando servidor backup grátis...")
            # Backup sem gradio_client
            import base64
            st.markdown("""
            <iframe src="https://facebook-musicgen.hf.space" width="100%" height="600"></iframe>
            """, unsafe_allow_html=True)
            st.markdown("Usa o gerador acima - é 100% grátis, gera na hora!")

st.markdown("---")
st.markdown("**👑 Isso é de verdade grátis:**")
st.markdown("- Sem API KEY\n- Sem pagar\n- Beat criado por IA na hora\n- Não é link Pixabay")
