import streamlit as st
import pandas as pd
from datetime import datetime

# --- CÓDIGO NOVO PARA ESCONDER MENU FEIO DOS CLIENTES ---
hide_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none!important;}
[data-testid="stToolbar"] {display:none!important;}
div[data-testid="stStatusWidget"] {display:none!important;}
[data-testid="manage-app-button"] {display:none!important;}
button[kind="header"] {display:none!important;}
#stDecoration {display:none;}
</style>
"""
st.markdown(hide_style, unsafe_allow_html=True)
# --- FIM DO CÓDIGO PARA ESCONDER ---

# --- TEU CÓDIGO ANTIGO DA DISTRIBUIDORA ---
st.set_page_config(page_title="King Slesha Moz", page_icon="👑", layout="centered")

st.markdown("""
<h1 style='text-align: center; color: gold; background-color: black; padding: 20px; border-radius: 10px;'>
👑 KING SLESHA MOZ - DISTRIBUIDORA
</h1>
""", unsafe_allow_html=True)

# Inicializa banco de dados na sessão
if 'artistas' not in st.session_state:
    st.session_state.artistas = []
if 'musicas' not in st.session_state:
    st.session_state.musicas = []

aba = st.selectbox("Menu", ["Criar Conta Artista", "Enviar Música", "Painel Admin"])

if aba == "Criar Conta Artista":
    st.subheader("Criar Conta Artista")
    st.write("Cada cliente só cria uma conta com Email ou Google para entrar na plataforma")

    nome = st.text_input("Nome Completo *")
    email = st.text_input("Email *", placeholder="seu@gmail.com")
    senha = st.text_input("Senha *", type="password")
    telefone = st.text_input("WhatsApp")

    if st.button("Criar Minha Conta 👑", use_container_width=True):
        if nome and email and senha:
            st.session_state.artistas.append({
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "data": datetime.now().strftime("%d/%m/%Y")
            })
            st.success(f"Conta criada com sucesso {nome}! Agora vai em 'Enviar Música'")
            st.balloons()
        else:
            st.error("Preenche Nome, Email e Senha!")

elif aba == "Enviar Música":
    st.subheader("Enviar Tua Música para Plataformas")

    artista_email = st.text_input("Teu Email cadastrado")
    titulo = st.text_input("Título da Música *")
    genero = st.selectbox("Gênero", ["Afrobeat", "Amapiano", "Hip Hop", "R&B", "Kizomba", "Outro"])
    arquivo = st.file_uploader("MP3 ou WAV *", type=["mp3", "wav"])
    capa = st.file_uploader("Capa 3000x3000 *", type=["jpg", "png", "jpeg"])

    if st.button("Enviar para King Slesha Moz 🚀", use_container_width=True):
        if titulo and arquivo and capa and artista_email:
            st.session_state.musicas.append({
                "titulo": titulo,
                "artista_email": artista_email,
                "genero": genero,
                "status": "Recebido - Aguardando envio para Spotify",
                "data": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            st.success("Música recebida! Vamos enviar para Spotify, Boomplay, Apple Music em 48h!")
        else:
            st.error("Preenche tudo!")

elif aba == "Painel Admin":
    st.subheader("Painel Admin - King Slesha Moz")
    senha_admin = st.text_input("Senha Admin", type="password")

    if senha_admin == "king2024":
        st.success("Bem vindo King!")

        st.write(f"### Total Artistas: {len(st.session_state.artistas)}")
        if st.session_state.artistas:
            st.dataframe(pd.DataFrame(st.session_state.artistas))

        st.write(f"### Total Músicas: {len(st.session_state.musicas)}")
        if st.session_state.musicas:
            df = pd.DataFrame(st.session_state.musicas)
            st.dataframe(df)

            # Marcar como enviado
            for i, musica in enumerate(st.session_state.musicas):
                col1, col2 = st.columns([3,1])
                with col1:
                    st.write(f"{musica['titulo']} - {musica['status']}")
                with col2:
                    if st.button(f"Marcar Enviado", key=f"env_{i}"):
                        st.session_state.musicas[i]['status'] = "Enviado para Plataformas ✅"
                        st.rerun()
    elif senha_admin:
        st.error("Senha errada!")

st.markdown("---")
st.markdown("<center>KingSlesha.com | 70% Artista / 30% King Slesha Moz</center>", unsafe_allow_html=True)
