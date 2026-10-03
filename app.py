import streamlit as st

st.set_page_config(page_title="King Slesha Moz", page_icon="👑")

st.markdown("""
<style>
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}
div[data-testid="stToolbar"] {visibility: hidden;}
div[data-testid="stDecoration"] {visibility: hidden;}
div[data-testid="stStatusWidget"] {visibility: hidden;}
/* TIRA O MANAGE APP DE BAIXO */
div[data-testid="stAppDeployButton"] {display: none;}
.stAppDeployButton {display: none;}
[data-testid="manage-app-button"] {display: none;}
</style>
""", unsafe_allow_html=True)

st.markdown("## 👑 King Slesha Moz")

precos = {
    "🎵 1 Beat - 500MT": 500,
    "🎵 3 Beats - 1200MT": 1200,
    "🎤 Musica Completa - 2500MT": 2500
}

escolha = st.selectbox("O que queres comprar?", list(precos.keys()))
valor = precos[escolha]

st.markdown(f"# Total: {valor} MT")
st.divider()

metodo = st.radio("Como queres pagar?", ["M-Pesa", "eMola"])
numero = st.text_input("📱 Escreve TEU numero de M-Pesa/eMola:", placeholder="84xxxxxxx")

if st.button(f"PAGAR {valor}MT AGORA", use_container_width=True):
    if len(numero) < 9:
        st.error("Numero invalido!")
    else:
        st.success(f"Pedido enviado para {numero}! Confirma no teu celular com teu PIN")
        st.balloons()
