import streamlit as st
st.set_page_config(page_title="King Slesha Pagamentos", page_icon="💰")

st.markdown("""
<h1 style='text-align:center'>👑 King Slesha - Loja Oficial</h1>
<p style='text-align:center'>Pagamento Seguro M-Pesa & eMola</p>
""", unsafe_allow_html=True)

# --- PREÇOS - VOCÊ PODE EDITAR AQUI ---
precos = {
    "🎵 1 Beat Amapiano - 500MT": 500,
    "🎵 3 Beats + Mixagem - 1200MT": 1200,
    "🎤 Música Completa + Autotune - 2500MT": 2500,
    "👑 Pacote Artista Completo - 5000MT": 5000
}

st.markdown("### 🛒 Escolhe o Pacote:")
escolha = st.selectbox("Pacote", list(precos.keys()))
valor = precos[escolha]
st.markdown(f"### 💰 Total: **{valor} MT**")

st.markdown("---")
st.markdown("### 📱 Pagamento")

metodo = st.radio("Escolhe:", ["📱 M-Pesa", "📱 eMola"])
numero = st.text_input("Teu número M-Pesa / eMola (ex: 84xxxxxxx)", placeholder="84xxxxxxx")

if st.button(f"💸 PAGAR {valor}MT com {metodo}"):
    if len(numero) < 9:
        st.error("Número inválido! Tem que ser 84xxxxxxx ou 82xxxxxxx")
    else:
        st.success(f"✅ Pedido enviado para {numero}!")
        st.info(f"""
        **O QUE ACONTECE AGORA:**
        1. Você vai receber uma mensagem no teu celular
        2. Vai pedir pra CONFIRMAR com teu PIN do {metodo}
        3. Digita teu PIN **NO TEU CELULAR** (não aqui no site!)
        4. Pagamento confirmado!
        """)
        st.markdown(f"""
        <div style='background:#f0f0f0;padding:15px;border-radius:10px'>
        <b>📲 Verifica teu celular agora!</b><br>
        Mensagem do {metodo} chegou para {numero}<br>
        Valor: {valor}MT - {escolha}
        </div>
        """, unsafe_allow_html=True)

        # AQUI VAI A INTEGRAÇÃO REAL COM API (precisa conta comerciante)
        st.warning("🔧 MODO TESTE: Pra funcionar de verdade, precisa ativar API M-Pesa. Me fala quando quiser ativar!")

st.markdown("---")
st.markdown("### 🔧 Como ativar pagamento de verdade (sem máfia):")

with st.expander("📱 Como ativar M-Pesa API (Vodacom)"):
    st.markdown("""
    1. Vai na loja Vodacom com NUIT e BI
    2. Pede conta **M-Pesa Business**
    3. Eles te dão **API Key**
    4. Cola API Key no código
    5. Aí o cliente recebe mensagem automática!
    """)

with st.expander("📱 Como ativar eMola API"):
    st.markdown("""
    1. Liga para 1221 (Movitel)
    2. Pede **eMola Negócio**
    3. Mesma coisa, te dão API
    """)

st.caption("👑 King Slesha - Pagamento 100% Seguro | Nunca pedimos teu PIN aqui!")
