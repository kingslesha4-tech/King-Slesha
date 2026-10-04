import streamlit as st
import datetime, random
import pandas as pd

PAYPAL_OFICIAL = "Kingslesha4@gmail.com"
SENHA_KING = "chila1990"

if "musicas" not in st.session_state:
    st.session_state["musicas"] = []
if "logado" not in st.session_state:
    st.session_state["logado"] = False

st.set_page_config(page_title="King Slesha Moz", page_icon="KING")
st.markdown("<h1 style='background:black;color:gold;text-align:center;padding:20px;border-radius:10px;'>KING SLESHA MOZ</h1>", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Menu", ["Enviar Musica", "Painel King"])

if menu == "Enviar Musica":
    with st.form("envio"):
        nome = st.text_input("Nome Artista *")
        email_a = st.text_input("Email Artista *")
        paypal_a = st.text_input("PayPal Artista 70% *")
        titulo = st.text_input("Titulo Musica *")
        genero = st.selectbox("Genero", ["Amapiano", "Afrobeat", "Hip Hop", "Marrabenta", "Pandza", "Outro"])
        mp3 = st.file_uploader("MP3/WAV *", type=["mp3","wav"])
        capa = st.file_uploader("Capa 3000x3000 *", type=["jpg","png"])
        ok = st.checkbox("Aceito contrato 70/30 *")
        btn = st.form_submit_button("ENVIAR PARA KING", use_container_width=True, type="primary")

        if btn:
            if not ok or not nome or not titulo or not mp3:
                st.error("Preenche tudo e coloca MP3!")
            else:
                isrc = "MZ-KSM-25-" + str(random.randint(10000,99999))
                nova = {
                    "Data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Artista": nome,
                    "Musica": titulo,
                    "Genero": genero,
                    "Email": email_a,
                    "PayPal Artista": paypal_a,
                    "ISRC": isrc,
                    "Status": "Pendente",
                    "mp3_bytes": mp3.read(),
                    "mp3_nome": mp3.name,
                    "capa_bytes": capa.read() if capa else None,
                    "capa_nome": capa.name if capa else None
                }
                st.session_state["musicas"].append(nova)
                st.success("Recebido! ISRC: " + isrc)
                st.balloons()

else:
    st.subheader("Painel King Slesha")

    if not st.session_state["logado"]:
        senha = st.text_input("Senha King", type="password", placeholder="Digite sua senha")
        if st.button("ENTRAR NO PAINEL", use_container_width=True, type="primary"):
            if senha.lower().strip() == SENHA_KING:
                st.session_state["logado"] = True
                st.rerun()
            else:
                st.error("Senha incorreta!")
    else:
        st.success("Bem-vindo King!")

        col1, col2, col3 = st.columns(3)
        total = len(st.session_state["musicas"])
        pendentes = len([m for m in st.session_state["musicas"] if m["Status"] == "Pendente"])
        col1.metric("Total Musicas", total)
        col2.metric("Pendentes", pendentes)
        col3.metric("Status", "Online")

        col4, col5 = st.columns(2)
        col4.metric("PayPal Oficial", PAYPAL_OFICIAL)
        col5.metric("Divisao", "70/30")

        st.write("---")
        st.subheader("Musicas para Ouvir, Baixar e Aprovar")

        if total == 0:
            st.info("Nenhuma musica ainda.")
        else:
            df = pd.DataFrame([{k:v for k,v in m.items() if k not in ["mp3_bytes","capa_bytes"]} for m in st.session_state["musicas"]])
            st.dataframe(df, use_container_width=True)
            st.write("---")

            for i in range(len(st.session_state["musicas"])):
                m = st.session_state["musicas"][i]
                artista = m["Artista"]
                musica = m["Musica"]
                status = m["Status"]
                isrc_val = m["ISRC"]
                email_val = m["Email"]
                paypal_val = m["PayPal Artista"]
                genero_val = m["Genero"]
                data_val = m["Data"]

                with st.expander("MUSICA: " + artista + " - " + musica + " | " + status):
                    st.write("Artista: " + artista + " | Email: " + email_val)
                    st.write("Genero: " + genero_val + " | Data: " + data_val)
                    st.write("ISRC: " + isrc_val + " | PayPal: " + paypal_val)

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write("OUVIR MUSICA:")
                        st.audio(m["mp3_bytes"])
                        st.download_button("BAIXAR MP3", m["mp3_bytes"], file_name=m["mp3_nome"], key=f"mp3_{i}")

                    with col_b:
                        if m["capa_bytes"]:
                            st.write("CAPA:")
                            st.image(m["capa_bytes"], width=200)
                            st.download_button("BAIXAR CAPA", m["capa_bytes"], file_name=m["capa_nome"], key=f"capa_{i}")

                    if status == "Pendente":
                        if st.button("APROVAR ESTA MUSICA", key=f"aprov_{i}", type="primary", use_container_width=True):
                            st.session_state["musicas"][i]["Status"] = "Aprovada"
                            st.success(musica + " Aprovada!")
                            st.rerun()
                    else:
                        st.success("Ja Aprovada")

        if st.button("SAIR"):
            st.session_state["logado"] = False
            st.rerun()
