import streamlit as st
import random
import datetime

st.set_page_config(page_title="King Slesha Moz", page_icon="👑", layout="wide")

# HEADER
st.markdown("""
<h1 style='color:gold; background:black; padding:20px; text-align:center;'>
👑 KING SLESHA MOZ DISTRIBUIDORA
</h1>
<p style='text-align:center;'>Marracuene - Maputo | PayPal Oficial: Kingslesha4@gmail.com | 70% Artista / 30% Label</p>
""", unsafe_allow_html=True)

menu = st.sidebar.selectbox("Menu King", ["Enviar Musica", "Painel King", "Banco King", "Status Spotify"])

# GERADOR ISRC E UPC
def gerar_isrc():
    return f"MZ-KSM-{datetime.datetime.now().year % 100}-{random.randint(10000,99999)}"

def gerar_upc():
    return f"1980{random.randint(100000000,999999999)}"

if menu == "Enviar Musica":
    st.subheader("🎵 Enviar sua música para distribuição")
    
    with st.form("form_musica"):
        nome_artista = st.text_input("Nome do Artista *")
        email_artista = st.text_input("Email do Artista *")
        paypal_artista = st.text_input("PayPal do Artista para receber 70% *", placeholder="ex: artista@gmail.com")
        titulo = st.text_input("Título da Música *", value="Lefty Raite")
        genero = st.selectbox("Gênero", ["Afro-House", "Amapiano", "Marrabenta", "Kizomba", "Outro"])
        arquivo = st.file_uploader("MP3 (WAV) *", type=["mp3","wav"])
        capa = st.file_uploader("Capa 3000x3000 *", type=["jpg","png"])
        
        st.markdown("---")
        st.markdown("**📄 CONTRATO 70/30 AUTOMÁTICO**")
        st.info("""
        Ao enviar, você concorda:
        - 70% dos royalties para você via PayPal
        - 30% para King Slesha Moz (taxa operacional)
        - Pagamento mensal até dia 15 via Banco King
        - Você mantém 100% dos direitos autorais
        - Distribuição em Spotify, Apple Music, Deezer, etc
        PayPal Oficial da Distribuidora: Kingslesha4@gmail.com
        """)
        aceito = st.checkbox("Li e aceito o contrato 70/30 *")
        
        enviar = st.form_submit_button("🚀 ENVIAR PARA ANALISE KING")
        
        if enviar and aceito and nome_artista and titulo:
            isrc = gerar_isrc()
            upc = gerar_upc()
            st.success(f"✅ Música recebida! ISRC: {isrc} | UPC: {upc}")
            st.balloons()
            st.write(f"Status: Pendente de aprovação no Painel King")
            # Aqui salva no Supabase: supabase.table("musicas").insert({...})

elif menu == "Painel King":
    st.subheader("👑 Painel de Aprovação - Só King Slesha")
    senha = st.text_input("Senha King", type="password")
    if senha == "king2025": # troca tua senha
        st.write("Músicas Pendentes:")
        st.markdown("""
        | Artista | Música | ISRC | PayPal | Ação |
        |---|---|---|---|---|
        | King Slesha | Lefty Raite | MZ-KSM-25-12345 | Kingslesha4@gmail.com | ✅ Aprovar |
        """)
        if st.button("Aprovar Lefty Raite"):
            st.success("Aprovada! Pronta pra subir pro Spotify quando for provider")
    else:
        st.warning("Área restrita ao King")

elif menu == "Banco King":
    st.subheader("💰 Banco King - Royalties")
    st.metric("PayPal Oficial Recebendo", "Kingslesha4@gmail.com", "Ativo")
    st.markdown("""
    | Data | Música | Valor Recebido | 70% Artista | 30% King | Status | Comprovante |
    |---|---|---|---|---|---|---|
    | 04/10/2025 | Lefty Raite | $0.00 | $0.00 | $0.00 | Aguardando Spotify | - |
    """)
    valor = st.number_input("Lançar royalty recebido do Spotify", min_value=0.0)
    if st.button("Dividir 70/30"):
        st.write(f"Artista recebe: ${valor*0.7:.2f} | King fica: ${valor*0.3:.2f}")

elif menu == "Status Spotify":
    st.subheader("📡 Status Candidatura Spotify Provider")
    st.info("Email enviado em 04/10/2025 para content-operations@spotify.com com Company Profile")
    st.progress(30)
    st.write("Aguardando resposta - Prazo: 15 a 30 dias")
    st.write("PayPal configurado: Kingslesha4@gmail.com")
    st.write("Próximo passo: Receber credenciais DDEX da Spotify")
