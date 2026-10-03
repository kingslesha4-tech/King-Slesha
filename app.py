import streamlit as st
st.set_page_config(page_title="King Slesha - Pagamentos", page_icon="💰", layout="centered")

TEU_MPESA = "853772668"
TEU_EMOLA = "874336850"
TEU_WHATSAPP = "258853772668"

st.markdown("""
<h1 style='text-align:center'>👑 King Slesha</h1>
<p style='text-align:center'>Beats & Músicas - Pagamento Oficial</p>
""", unsafe_allow_html=True)

# --- TEUS PREÇOS ---
precos = {
    "🎵 1 Beat Amapiano - 500MT": 500,
    "🎵 3 Beats + Mixagem - 1200MT": 1200,
    "🎤 Música Completa + Autotune - 2500MT": 2500,
    "👑 Pacote Artista Completo - 5000MT": 5000
}

escolha = st.selectbox("🛒 Escolhe o que queres comprar:", list(precos.keys()))
valor = precos[escolha]

st.markdown(f"<h2 style='text-align:center;color:#00a651'>💰 Total: {valor} MT</h2>", unsafe_allow_html=True)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    metodo = st.radio("Pagar com:", ["📱 M-Pesa", "📱 eMola"])

numero_destino = TEU_MPESA if "M-Pesa" in metodo else TEU_EMOLA
cor = "#EB0000" if "M-Pesa" in metodo else "#FF6A00"

st.markdown(f"""
<div style='background:{cor};color:white;padding:20px;border-radius:12px;text-align:center'>
<b style='font-size:14px'>ENVIA {valor}MT PARA:</b><br>
<span style='font-size:32px;font-weight:bold'>📱 {numero_destino}</span><br>
<span style='font-size:14px'>Nome: King Slesha<br>Confirma o nome antes de enviar!</span>
</div>
""", unsafe_allow_html=True)

st.info(f"""
**Como pagar no {metodo}:**
1. Marca *840# (M-Pesa) ou *898# (eMola)
2. Escolhe **1 - Enviar dinheiro**
3. Número: **{numero_destino}**
4. Valor: **{valor}**
5. Digita teu **PIN NO TEU CELULAR** para confirmar
""")

st.markdown("---")
st.markdown("### ✅ Já fizeste o pagamento?")

numero_cliente = st.text_input("📱 Teu número que enviou o dinheiro:", placeholder="Ex: 84xxxxxxx")
id_transacao = st.text_input("🔢 ID da transação (vem na SMS):", placeholder="Ex: PP1234ABCD")

if st.button("✅ JÁ PAGUEI - CONFIRMAR", use_container_width=True):
    if len(numero_cliente) < 9 or len(id_transacao) < 4:
        st.error("⚠️ Escreve teu número e o ID da transação!")
    else:
        st.success("🎉 Pagamento registrado!")
        st.balloons()
        msg = f"Ola King Slesha! Acabei de pagar {valor}MT para {escolha}. Meu numero: {numero_cliente} ID: {id_transacao} Metodo: {metodo}"
        import urllib.parse
        link = f"https://wa.me/{TEU_WHATSAPP}?text={urllib.parse.quote(msg)}"
        st.markdown(f"""
        <a href="{
