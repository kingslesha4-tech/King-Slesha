import streamlit as st

st.set_page_config(page_title="King Slesha Moz", page_icon="🎬")

CODIGO = "1245496"
NOME = "KING SLESHA MOZ"
NUMERO = "853772668"
VALOR = "50"

st.title("King Slesha Moz - Filmes")
st.markdown(f"### {VALOR} MZN / 48 horas")
st.success(f"Codigo M-Pesa: {CODIGO} - {NOME}")

st.divider()
st.markdown("#### COMO PAGAR:")
st.markdown(f"1. Digita *150*00#")
st.markdown(f"2. Escolhe 4. Pagar")
st.markdown(f"3. Escolhe Empresa")
st.markdown(f"4. Codigo: {CODIGO}")
st.markdown(f"5. Valor: {VALOR}")
st.markdown(f"6. PIN")

st.divider()
st.markdown("#### Depois de pagar, confirma aqui:")

numero_cliente = st.text_input("Seu numero que pagou", placeholder="84xxxxxxx")
id_trans = st.text_input("ID da transacao (opcional)", placeholder="PP...")

if st.button(f"JA PAGUEI {VALOR} MZN PARA {CODIGO}", type="primary"):
    if not numero_cliente:
        st.error("Digite seu numero")
    else:
        st.balloons()
        st.success(f"Verificando pagamento de {numero_cliente} para {CODIGO}")
        link = f"https://wa.me/258{NUMERO}?text=Ola%20KING%20paguei%20{VALOR}MZN%20de%20{numero_cliente}%20para%20{CODIGO}%20ID%20{id_trans}"
        st.markdown(f"[CLICAR PARA ENVIAR NO WHATSAPP]({link})")
        st.info(f"Envia comprovativo para {NUMERO} no WhatsApp")

st.caption(f"Suporte {NUMERO} | Codigo {CODIGO} | Quando pagas para {CODIGO}, eu recebo no {NUMERO}")
