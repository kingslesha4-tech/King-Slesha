import streamlit as st
import urllib.parse

st.set_page_config(page_title="King Slesha - Pagamentos", page_icon="💰")

TEU_MPESA = "853772668"
TEU_EMOLA = "874336850"
TEU_WHATSAPP = "258853772668"

st.title("👑 King Slesha")
st.markdown("**Beats & Musicas - Pagamento Oficial**")

precos = {
    "🎵 1 Beat Amapiano - 500MT": 500,
    "🎵 3 Beats + Mixagem - 1200MT": 1200,
    "🎤 Musica Completa + Autotune - 2500MT": 2500,
    "👑 Pacote Artista Completo - 5000MT": 5000
}

escolha = st.selectbox("Escolhe o que queres comprar:", list(precos.keys()))
valor = precos[escolha]

st.markdown("## Total: " + str(valor) + " MT")

st.divider()
metodo = st.radio("Pagar com:", ["M-Pesa", "eMola"])

if "M-Pesa" in metodo:
    numero_destino = TEU_MPESA
    cor = "#EB0000"
else:
    numero_destino = TEU_EMOLA
    cor = "#FF6A00"

st.markdown("### ENVIA " + str(valor) + "MT PARA:")
st.markdown("### 📱 " + numero_destino)
st.markdown("Nome: King Slesha")

st.info("Como pagar: Marca *840# > 1-Enviar dinheiro > Numero: " + numero_destino + " > Valor: " + str(valor) + " > PIN no teu celular")

st.divider()
st.markdown("### Ja pagaste?")

numero_cliente = st.text_input("Teu numero que enviou:", placeholder="84xxxxxxx")
id_transacao = st.text_input("ID da transacao (SMS):", placeholder="PP1234ABCD")

if st.button("JA PAGUEI - CONFIRMAR", use_container_width=True):
    if len(numero_cliente) < 9 or len(id_transacao) < 4:
        st.error("Escreve teu numero e ID!")
    else:
        st.success("Pagamento registrado!")
        st.balloons()
        mensagem = "Ola King! Paguei " + str(valor) + "MT para " + escolha + ". Meu numero: " + numero_cliente + " ID: " + id_transacao + " Metodo: " + metodo
        link = "https://wa.me/" + TEU_WHATSAPP + "?text=" + urllib.parse.quote(mensagem)
        st.link_button("📲 ENVIAR COMPROVATIVO NO WHATSAPP", link, use_container_width=True)
        st.markdown("Vou te enviar o " + escolha + " em 5 min!")
