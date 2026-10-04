import streamlit as st
import datetime
import random
import pandas as pd
import time

PAYPAL_OFICIAL = "Kingslesha4@gmail.com"
SENHA_KING = "chila1990"
EMAIL_KING = "kingslesha4@gmail.com"

if "musicas" not in st.session_state:
    st.session_state["musicas"] = []
if "pagamentos" not in st.session_state:
    st.session_state["pagamentos"] = []
if "users" not in st.session_state:
    st.session_state["users"] = []
if "logado" not in st.session_state:
    st.session_state["logado"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
if "is_king" not in st.session_state:
    st.session_state["is_king"] = False

st.set_page_config(page_title="King Slesha Moz", page_icon="KING")
st.markdown("<h1 style='background:black;color:gold;text-align:center;padding:20px;border-radius:10px;'>KING SLESHA MOZ - DISTRIBUIDORA</h1>", unsafe_allow_html=True)

def registar_user(nome, email, senha):
    for u in st.session_state["users"]:
        if u.get("email","").lower() == email.lower():
            return False
    novo = {"nome": nome, "email": email.lower(), "senha": senha, "data": datetime.datetime.now().strftime("%d/%m/%Y")}
    st.session_state["users"].append(novo)
    return True

def login_user(email, senha):
    em = email.lower()
    if em == EMAIL_KING.lower():
        if senha == SENHA_KING:
            st.session_state["is_king"] = True
            st.session_state["logado"] = True
            st.session_state["current_user"] = {"nome": "King Slesha", "email": email}
            return True
    for u in st.session_state["users"]:
        ue = u.get("email","").lower()
        us = u.get("senha","")
        if ue == em:
            if us == senha:
                st.session_state["current_user"] = u
                st.session_state["is_king"] = False
                st.session_state["logado"] = True
                return True
    return False

# MENU
if not st.session_state["logado"]:
    menu = st.sidebar.selectbox("Menu", ["Login", "Registar", "Painel King"])
else:
    if st.session_state["is_king"]:
        menu = st.sidebar.selectbox("Menu King", ["Painel King", "Sair"])
    else:
        menu = st.sidebar.selectbox("Menu Artista", ["Enviar Musica", "Minhas Musicas", "Sair"])
        st.sidebar.success("Logado: " + st.session_state["current_user"].get("nome",""))

# REGISTAR - CADA CLIENTE CRIA CONTA
if menu == "Registar" and not st.session_state["logado"]:
    st.subheader("Criar Conta - Cada cliente cria sua conta")
    st.write("Cria conta com Email ou entra com Google")
    nome_r = st.text_input("Nome Completo *")
    email_r = st.text_input("Email *", placeholder="seu@gmail.com")
    senha_r = st.text_input("Senha *", type="password")
    senha_r2 = st.text_input("Confirmar Senha *", type="password")
    if st.button("CRIAR CONTA COM EMAIL", type="primary", use_container_width=True):
        if not nome_r or not email_r or not senha_r:
            st.error("Preenche tudo!")
        elif senha_r!= senha_r2:
            st.error("Senhas diferentes!")
        else:
            if registar_user(nome_r, email_r, senha_r):
                st.success("Conta criada! Agora vai em Login!")
                st.balloons()
            else:
                st.error("Email ja existe! Faz Login")
    st.write("---")
    st.write("Ou entrar com conta Google")
    email_g = st.text_input("Seu Gmail do Google", placeholder="seu@gmail.com", key="gmail_reg")
    if st.button("CONTINUAR COM GOOGLE", use_container_width=True):
        if email_g:
            nome_g = email_g.split("@")[0]
            registar_user(nome_g, email_g, "google123")
            login_user(email_g, "google123")
            st.success("Entrou com Google!")
            st.rerun()

# LOGIN
if menu == "Login" and not st.session_state["logado"]:
    st.subheader("Entrar na Plataforma")
    st.write("Entra com Email ou Google")
    email_l = st.text_input("Email *", placeholder="seu@gmail.com", key="email_login")
    senha_l = st.text_input("Senha *", type="password", key="senha_login")
    if st.button("ENTRAR COM EMAIL", type="primary", use_container_width=True):
        if login_user(email_l, senha_l):
            st.rerun()
        else:
            st.error("Email ou senha errada!")
    st.write("---")
    email_g2 = st.text_input("Ou seu Gmail Google", placeholder="seu@gmail.com", key="gmail_login")
    if st.button("ENTRAR COM GOOGLE", use_container_width=True):
        if email_g2:
            encontrou = False
            for u in st.session_state["users"]:
                if u.get("email","").lower() == email_g2.lower():
                    st.session_state["current_user"] = u
                    st.session_state["logado"] = True
                    st.session_state["is_king"] = False
                    encontrou = True
                    st.rerun()
            if not encontrou:
                registar_user(email_g2.split("@")[0], email_g2, "google123")
                login_user(email_g2, "google123")
                st.rerun()
    st.info("Nao tem conta? Vai em Registar")

# ENVIAR MUSICA - CODIGO ANTIGO COMPLETO DE VOLTA
if menu == "Enviar Musica" and st.session_state["logado"] and not st.session_state["is_king"]:
    cur = st.session_state["current_user"]
    user_nome = cur.get("nome","")
    user_email = cur.get("email","")
    st.subheader("Enviar Musica")
    st.write("Logado como: " + user_nome)
    nome = st.text_input("Nome Artista *", value=user_nome)
    email_a = st.text_input("Email Artista *", value=user_email)
    titulo = st.text_input("Titulo Musica *")
    # GENERO COM KIZOMBA DE VOLTA - TEU CODIGO ANTIGO
    genero = st.selectbox("Genero", ["Amapiano", "Afrobeat", "Hip Hop", "Marrabenta", "Pandza", "Kizomba", "Zouk", "Afro House", "R&B", "Outro"])
    st.write("---")
    st.subheader("Forma de Receber 70%")
    forma_pag = st.selectbox("Escolhe como quer receber", ["PayPal", "M-Pesa", "e-Mola", "Conta Bancaria"])
    paypal_a = ""
    mpesa_num = ""
    emola_num = ""
    banco_nome = ""
    banco_conta = ""
    banco_nib = ""
    if forma_pag == "PayPal":
        paypal_a = st.text_input("Seu PayPal 70% *", placeholder="seu@gmail.com")
    if forma_pag == "M-Pesa":
        mpesa_num = st.text_input("Seu Numero M-Pesa *", placeholder="84xxxxxxx")
    if forma_pag == "e-Mola":
        emola_num = st.text_input("Seu Numero e-Mola *", placeholder="82xxxxxxx")
    if forma_pag == "Conta Bancaria":
        banco_nome = st.selectbox("Banco", ["BCI", "Millennium BIM", "Standard Bank", "Moza Banco", "ABSA", "Outro"])
        banco_conta = st.text_input("Numero da Conta *")
        banco_nib = st.text_input("NIB *", placeholder="0000...")
    st.write("---")
    mp3 = st.file_uploader("MP3/WAV/M4A *", type=["mp3","wav","m4a"])
    capa = st.file_uploader("Capa 3000x3000 *", type=["jpg","png","jpeg"])
    ok = st.checkbox("Aceito contrato 70/30")
    if st.button("ENVIAR PARA KING", use_container_width=True, type="primary"):
        if not ok or not nome or not titulo or not mp3:
            st.error("Preenche tudo!")
        else:
            # TRACO DE PROGRESSO ANTIGO DE VOLTA
            texto = st.empty()
            barra = st.progress(0)
            texto.write("Iniciando envio 0%")
            barra.progress(10)
            time.sleep(0.3)
            texto.write("Salvando MP3 30%")
            barra.progress(30)
            time.sleep(0.3)
            texto.write("Salvando capa 60%")
            barra.progress(60)
            time.sleep(0.3)
            texto.write("Gerando ISRC 85%")
            barra.progress(85)
            time.sleep(0.3)
            isrc = "MZ-KSM-25-" + str(random.randint(10000,99999))
            mp3_data = mp3.getvalue()
            capa_data = capa.getvalue() if capa else None
            nova = {
                "Data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Artista": nome,
                "Musica": titulo,
                "Genero": genero,
                "Email": email_a,
                "Email Dono": user_email,
                "Forma Pag": forma_pag,
                "PayPal Artista": paypal_a,
                "M-Pesa": mpesa_num,
                "e-Mola": emola_num,
                "Banco": banco_nome,
                "Conta": banco_conta,
                "NIB": banco_nib,
                "ISRC": isrc,
                "Status": "Pendente",
                "Enviado Plataforma": "Nao",
                "Data Envio Plat": "",
                "Plataformas": "",
                "mp3_bytes": mp3_data,
                "mp3_nome": mp3.name,
                "capa_bytes": capa_data,
                "capa_nome": capa.name if capa else None
            }
            st.session_state["musicas"].append(nova)
            barra.progress(100)
            texto.write("Concluido 100% - Musica terminou!")
            st.success("Recebido! ISRC " + isrc)
            st.balloons()

# MINHAS MUSICAS
if menu == "Minhas Musicas" and st.session_state["logado"] and not st.session_state["is_king"]:
    st.subheader("Minhas Musicas")
    user_email = st.session_state["current_user"].get("email","")
    minhas = []
    for m in st.session_state["musicas"]:
        if m.get("Email Dono","").lower() == user_email.lower() or m.get("Email","").lower() == user_email.lower():
            minhas.append(m)
    if len(minhas) == 0:
        st.info("Ainda nao enviaste musica. Vai em Enviar Musica")
    else:
        st.write("Total: " + str(len(minhas)) + " musicas")
        for m in minhas:
            tit = m.get("Musica","") + " - " + m.get("Status","") + " - " + m.get("ISRC","")
            with st.expander(tit):
                st.write("Genero: " + m.get("Genero","") + " | Forma: " + m.get("Forma Pag",""))
                st.write("Status: " + m.get("Status","") + " | Enviado Plataforma: " + m.get("Enviado Plataforma","Nao"))
                if m.get("mp3_bytes"):
                    st.audio(m.get("mp3_bytes"), format="audio/mp3")
                    st.download_button("BAIXAR MUSICA", m.get("mp3_bytes"), file_name=m.get("mp3_nome","musica.mp3"), key="minha_mp3_" + m.get("ISRC",""))
                if m.get("capa_bytes"):
                    st.image(m.get("capa_bytes"), width=200)
                    st.download_button("BAIXAR CAPA", m.get("capa_bytes"), file_name=m.get("capa_nome","capa.jpg"), key="minha_capa_" + m.get("ISRC",""))

# PAINEL KING - CODIGO ANTIGO COMPLETO DE VOLTA
if menu == "Painel King":
    st.subheader("Painel King Slesha")
    if not st.session_state["logado"] or not st.session_state["is_king"]:
        email_k = st.text_input("Email King", value="kingslesha4@gmail.com")
        senha_k = st.text_input("Senha King", type="password", placeholder="chila1990")
        if st.button("ENTRAR NO PAINEL", use_container_width=True, type="primary"):
            if login_user(email_k, senha_k):
                st.rerun()
            else:
                st.error("Senha incorreta!")
    else:
        st.success("Bem-vindo King!")
        total = len(st.session_state["musicas"])
        pend = 0
        env = 0
        for mm in st.session_state["musicas"]:
            if mm.get("Status","") == "Pendente":
                pend = pend + 1
            if mm.get("Enviado Plataforma","") == "Sim":
                env = env + 1
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Musicas", total)
        col2.metric("Pendentes", pend)
        col3.metric("Enviadas Plat", env)
        col4.metric("Usuarios", len(st.session_state["users"]))
        col5, col6 = st.columns(2)
        col5.metric("PayPal Oficial", PAYPAL_OFICIAL)
        col6.metric("Divisao", "70/30")
        st.write("---")
        aba1, aba2, aba3 = st.tabs(["MUSICAS PARA OUVIR E APROVAR", "PAGAMENTOS DAS PLATAFORMAS", "USUARIOS"])
        with aba1:
            if total == 0:
                st.info("Nenhuma musica ainda")
            else:
                df = pd.DataFrame([{k:v for k,v in m.items() if k not in ["mp3_bytes","capa_bytes"]} for m in st.session_state["musicas"]])
                st.dataframe(df, use_container_width=True)
                st.write("---")
                for i in range(len(st.session_state["musicas"])):
                    m = st.session_state["musicas"][i]
                    artista = m.get("Artista","")
                    musica = m.get("Musica","")
                    status = m.get("Status","")
                    enviado = m.get("Enviado Plataforma","Nao")
                    tit = "MUSICA " + artista + " - " + musica + " - " + status + " - Plat: " + enviado
                    with st.expander(tit):
                        st.write("Artista: " + artista + " | Genero: " + m.get("Genero","") + " | Email: " + m.get("Email",""))
                        st.write("Forma: " + m.get("Forma Pag","") + " | ISRC: " + m.get("ISRC","") + " | Data: " + m.get("Data",""))
                        # MUSICA E CAPA DE VOLTA - OS DOIS
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.write("**MUSICA PARA OUVIR E BAIXAR**")
                            if m.get("mp3_bytes"):
                                if len(m.get("mp3_bytes")) > 100:
                                    st.audio(m.get("mp3_bytes"), format="audio/mp3")
                                    k1 = "mp3_" + str(i)
                                    st.download_button("BAIXAR MUSICA", m.get("mp3_bytes"), file_name=m.get("mp3_nome","musica.mp3"), key=k1, use_container_width=True)
                        with col_b:
                            st.write("**CAPA**")
                            if m.get("capa_bytes"):
                                st.image(m.get("capa_bytes"), width=250)
                                k2 = "capa_" + str(i)
                                st.download_button("BAIXAR CAPA", m.get("capa_bytes"), file_name=m.get("capa_nome","capa.jpg"), key=k2, use_container_width=True)
                        st.write("---")
                        if status == "Pendente":
                            k3 = "aprov_" + str(i)
                            if st.button("APROVAR ESTA MUSICA", key=k3, type="primary", use_container_width=True):
                                st.session_state["musicas"][i]["Status"] = "Aprovada"
                                st.rerun()
                        else:
                            st.success("Ja Aprovada")
                            if enviado == "Nao":
                                st.write("**Enviar para plataformas?**")
                                plats = st.multiselect("Escolhe plataformas", ["Spotify", "Apple Music", "Boomplay", "Audiomack", "YouTube Music", "Deezer", "TikTok", "Todas"], key="plat_" + str(i))
                                if st.button("MARCAR COMO ENVIADO PARA PLATAFORMA", key="env_" + str(i), use_container_width=True):
                                    st.session_state["musicas"][i]["Enviado Plataforma"] = "Sim"
                                    st.session_state["musicas"][i]["Data Envio Plat"] = datetime.datetime.now().strftime("%d/%m/%Y")
                                    txt = ", ".join(plats) if plats else "Todas"
                                    st.session_state["musicas"][i]["Plataformas"] = txt
                                    st.success("Marcado como enviado!")
                                    st.rerun()
                            else:
                                st.info("Enviado em " + m.get("Data Envio Plat","") + " para " + m.get("Plataformas",""))
        with aba2:
            st.subheader("Pagamentos das Plataformas - Quando plataforma pagou")
            with st.expander("ADICIONAR PAGAMENTO RECEBIDO DA PLATAFORMA"):
                if total == 0:
                    st.warning("Nenhuma musica ainda")
                else:
                    lista_musicas = []
                    for mm in st.session_state["musicas"]:
                        lista_musicas.append(mm.get("Musica","") + " - " + mm.get("Artista","") + " (" + mm.get("ISRC","") + ")")
                    musica_escolhida = st.selectbox("Escolhe musica", lista_musicas)
                    plataforma_pag = st.selectbox("Plataforma que pagou", ["Spotify", "Apple Music", "Boomplay", "Audiomack", "YouTube Music", "Deezer", "TikTok", "DistroKid", "Outro"])
                    valor_total = st.number_input("Valor total recebido (USD)", min_value=0.0, step=0.1)
                    data_pag = st.date_input("Data do pagamento", datetime.date.today())
                    obs = st.text_input("Observacao", placeholder="Ex: Pagamento Janeiro 2025")
                    if st.button("REGISTRAR PAGAMENTO", type="primary", use_container_width=True):
                        if valor_total > 0:
                            a70 = valor_total * 0.7
                            k30 = valor_total * 0.3
                            novo_pag = {
                                "Data Pagamento": data_pag.strftime("%d/%m/%Y"),
                                "Musica": musica_escolhida,
                                "Plataforma": plataforma_pag,
                                "Valor Total USD": valor_total,
                                "70% Artista USD": round(a70,2),
                                "30% King USD": round(k30,2),
                                "Obs": obs
                            }
                            st.session_state["pagamentos"].append(novo_pag)
                            st.success("Pagamento registrado! Artista $" + str(round(a70,2)) + " | King $" + str(round(k30,2)))
                            st.balloons()
            st.write("---")
            if len(st.session_state["pagamentos"]) == 0:
                st.info("Nenhum pagamento registrado ainda. Quando Spotify pagar, adiciona aqui.")
            else:
                df_pag = pd.DataFrame(st.session_state["pagamentos"])
                st.dataframe(df_pag, use_container_width=True)
                total_rec = 0
                total_art = 0
                total_king = 0
                for p in st.session_state["pagamentos"]:
                    total_rec = total_rec + p.get("Valor Total USD",0)
                    total_art = total_art + p.get("70% Artista USD",0)
                    total_king = total_king + p.get("30% King USD",0)
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Recebido", "$" + str(round(total_rec,2)))
                c2.metric("Total Artistas 70%", "$" + str(round(total_art,2)))
                c3.metric("Total King 30%", "$" + str(round(total_king,2)))
        with aba3:
            st.subheader("Usuarios Registrados - Contas criadas")
            if len(st.session_state["users"]) == 0:
                st.info("Nenhum usuario ainda")
            else:
                df_u = pd.DataFrame(st.session_state["users"])
                st.dataframe(df_u, use_container_width=True)

if menu == "Sair":
    st.session_state["logado"] = False
    st.session_state["current_user"] = None
    st.session_state["is_king"] = False
    st.rerun()
