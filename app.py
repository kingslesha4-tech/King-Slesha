import streamlit as st

st.set_page_config(page_title="King Slesha Moz - Filmes", page_icon="🎬")

st.title("🎬 King Slesha Moz")
st.subheader("Filmes 50 MZN / 48h")

st.markdown(f"""
### 💳 Pagar M-Pesa
**Código Comerciante:** `1245496`
**Número:** `853772668`
**Valor:** 50 MZN
""")

numero = st.text_input("Seu número M-Pesa (84... ou 82...)")

if st.button("PAGAR 50 MZN - Código 1245496", type="primary"):
    if numero:
        st.success(f"✅ Pedido enviado! Verifique seu {numero}")
        st.info(f"Você vai receber solicitação para pagar 50 MZN para KING SLESHA MOZ (1245496). Digite seu PIN M-Pesa para confirmar.")
        st.balloons()
    else:
        st.error("Digite seu número M-Pesa")

st.divider()
st.caption("Suporte: 853772668 | Código: 1245496 | Matola")
