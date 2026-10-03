import streamlit as st
import json, os
from datetime import datetime

st.set_page_config(page_title="King Slesha Moz - Carteira", page_icon="👑")

# ESCONDE O MANAGE APP
st.markdown("""
<style>
header, footer, #MainMenu {visibility: hidden;}
div[data-testid="stToolbar"] {display:none;}
.stAppDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

ARQUIVO = "carteiras.json"
if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w") as f: json.dump({}, f)

def load():
    with open(ARQUIVO, "r") as f: return json.load(f)
def save(d):
    with open(ARQUIVO, "w") as f: json.dump(d, f, indent=2)

precos = {"🎵 1 Beat - 500MT": 500, "🎵 3 Beats - 1200MT": 1200, "🎤 Completa - 2500MT": 2500}

st.markdown("## 👑 King Slesha Moz - Minha Carteira")
st.caption("Carteira de créditos para compra de beats. Não é banco. Pagamentos para M-Pesa 853772668")

tel = st.text_input("📱 Teu número (teu login):", placeholder="84xxxxxxx")

if len(tel) >= 9:
    dados = load()
    if tel not in dados:
        dados[tel] = {"saldo": 0, "historico": []}
        save(dados)

    saldo = dados[tel]["saldo"]
    st.metric("Teu Saldo Atual", f"{saldo} MT")

    tab1, tab2, tab3 = st.tabs(["🛒 Comprar", "💰 Carregar", "📜 Histórico"])

    with tab1:
        escolha = st.selectbox("O que queres?", list(precos.keys()))
        valor = precos[escolha]
        if st.button(f"Comprar por {valor}MT", use_container_width=True):
            if saldo >= valor:
                dados[tel]["saldo"] -= valor
                dados[tel]["historico"].append(f"{datetime.now().strftime('%d/%m %H:%M')} - COMPROU {escolha} -{valor}MT")
                save(dados)
                st.success("Beat liberado! Vou te enviar no WhatsApp!")
                st.balloons()
            else:
                st.error(f"Saldo insuficiente! Precisas de {valor}MT, tens {saldo}MT. Vai em Carregar.")

    with tab2:
        st.info("1. Envia M-Pesa para **853772668 - King Slesha**\n2. Escreve o ID da transação abaixo")
        id_trans = st.text_input("ID da transação M-Pesa:")
        valor_dep = st.number_input("Valor que enviaste:", min_value=100, step=100)
        if st.button("Enviar comprovativo"):
            if id_trans:
                # Aqui tu vais verificar manualmente no teu M-Pesa
                dados[tel]["saldo"] += valor_dep
                dados[tel]["historico"].append(f"{datetime.now().strftime('%d/%m %H:%M')} - CARREGAMENTO +{valor_dep}MT - ID:{id_trans} (Pendente verificação)")
                save(dados)
                st.success(f"Recebido! {valor_dep}MT adicionado. Vou confirmar no M-Pesa e liberar.")
            else:
                st.warning("Escreve o ID da transação")

    with tab3:
        for h in reversed(dados[tel]["historico"][-20:]):
            st.write(h)

# PAINEL ADMIN SÓ PRA TI
st.divider()
with st.expander("🔐 Painel Admin (só dono)"):
    senha = st.text_input("Senha admin:", type="password")
    if senha == "king2024":
        st.write(load())
        st.caption("Aqui vês todos saldos. Tu tens que conferir teu M-Pesa 853772668 antes de aprovar.")
