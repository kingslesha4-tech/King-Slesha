import streamlit as st
import urllib.parse

st.set_page_config(page_title="King Slesha Pay", page_icon="💰")

TEU_MPESA = "853772668"
TEU_EMOLA = "874336850"
TEU_WHATSAPP = "258853772668"

st.title("👑 King Slesha")
st.markdown("Pagamento Seguro")

precos = {
    "🎵 1 Beat - 500MT": 500,
    "🎵 3 Beats - 1200MT": 1200,
    "🎤 Musica Completa - 2500MT": 2500,
    "👑 Pacote Artista - 5000MT": 5000
}

escolha = st.selectbox("O que queres comprar?", list(precos.keys()))
valor = precos[escolha]
st.markdown(f"## Total: {valor} MT")

st.divider()

metodo = st.radio("Como queres pagar?", ["M-Pesa", "eMola"])
numero_cliente = st.text_input("📱 Escreve TEU numero de M-Pesa/eMola:", placeholder="84xxxxxxx ou 82xxxxxxx")

if st.button(f"PAGAR {valor}MT AGORA", use_container_width=True):
    if len(numero_cliente) < 9:
        st.error("Escreve teu numero certo! Ex: 84xxxxxxx")
    else:
        st.success(f"✅ Pedido enviado para {numero_cliente}!")
        st.markdown(f"""
        ### 📲 AGORA VERIFICA TEU CELULAR!

        Enviamos um pedido para o numero **{numero_cliente}**

        **1.** Vais receber uma mensagem do **{metodo}** agora
        **2.** Abre a mensagem no teu celular
        **3.** Confirma com **TEU PIN sozinho** no teu celular
        **4.** Ninguem ve teu PIN, so voce!
        """)

        if "M-Pesa" in metodo:
            st.info(f"Se nao receber mensagem, marca *840# > Enviar dinheiro > Para: {TEU_MPESA} > Valor: {valor}MT")
        else:
            st.info(f"Se nao receber mensagem, marca *898# > Enviar dinheiro > Para: {TEU_EMOLA} > Valor: {valor}MT")

        st.divider()
        st.markdown("### Ja confirmaste no teu celular?")
        id_trans = st.text_input("Coloca ID da transacao que recebeste por SMS:", key="id")

        if st.button("✅ JA CONFIRMEI NO MEU CELULAR"):
            msg = f"Ola King! Paguei {valor}MT - {escolha}. Meu numero: {numero_cliente} ID: {id_trans} - {metodo}"
            link = f"https://wa.me/{TEU_WHATSAPP}?text={urllib.parse.quote(msg)}"
            st.link_button("📲 ENVIAR COMPROVATIVO NO WHATSAPP", link, use_container_width=True)
            st.balloons()

st.caption(f"Recebedor: M-Pesa {TEU_MPESA} | eMola {TEU_EMOLA} | PIN so no teu celular, seguro!")
