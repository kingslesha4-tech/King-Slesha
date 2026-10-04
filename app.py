import streamlit as st, datetime, random, string
from supabase import create_client

SUPABASE_URL = "https://hfjskhhjrdjuphkbjdpu.supabase.co"
SUPABASE_KEY = "sb_publishable_gBj-IUXwTe8E1olKTLRBhg_l87QRjXu"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# CONFIG - TEU PAYPAL
PAYPAL_OFICIAL = "Kingslesha4@gmail.com"
MOZA_CONTA = "MOZA BANCO - KING SLESHA"
TAXA_ARTISTA = 70
TAXA_KING = 30

st.set_page_config(page_title="KING V15 OFICIAL", page_icon="👑", layout="centered")
st.markdown(f"""<div style="text-align:center;background:linear-gradient(90deg,black,#FFD700);padding:20px;border-radius:15px;">
<h1 style="color:white;margin:0;">👑 KING SLESHA MOZ V15</h1>
<p style="color:black;font-weight:bold;">PayPal: {PAYPAL_OFICIAL} | TAXA {TAXA_ARTISTA}/{TAXA_KING} | Moza Banco</p>
</div><br>""", unsafe_allow_html=True)

def gen_codes(): return f"MZ-{''.join(random.choices(string.ascii_uppercase, k=3))}-{datetime.datetime.now().year}-{''.join(random.choices(string.digits, k=5))}", ''.join(random.choices(string.digits, k=12))
def upload_file(b, f):
    try:
        n = f"{datetime.datetime.now().timestamp()}_{f.name.replace(' ','_')}"
        supabase.storage.from_(b).upload(n, f.getvalue(), {"content-type": f.type})
        return supabase.storage.from_(b).get_public_url(n)
    except: return None
def listar():
    try: return supabase.table("musicas").select("*").order("created_at", desc=True).execute().data
    except: return []
def listar_ganhos():
    try: return supabase.table("ganhos").select("*").order("created_at", desc=True).execute().data
    except: return []

menu = st.selectbox("MENU OFICIAL", ["🏠 CATÁLOGO", "🚀 SOU ARTISTA", "🔐 PAINEL KING", "💰 BANCO - Kingslesha4@gmail.com"])

if menu == "🏠 CATÁLOGO":
    aprovadas = [m for m in listar() if m.get('status')=='aprovada']
    if not aprovadas: st.info("Nenhuma música aprovada ainda. Seja o primeiro!")
    else:
        t1,t2 = st.tabs(["🎧 Spotify", "📺 YouTube"])
        with t1:
            for m in aprovadas:
                with st.container(border=True):
                    c1,c2 = st.columns([1,2])
                    with c1:
                        if m.get('capa_url'): st.image(m['capa_url'], use_container_width=True)
                    with c2:
                        st.markdown(f"**{m['titulo']}** - {m['artista']}")
                        st.caption(f"ISRC {m.get('isrc','')}")
                        if m.get('audio_url'): st.audio(m['audio_url'])
        with t2:
            for m in aprovadas:
                with st.container(border=True):
                    if m.get('capa_url'): st.image(m['capa_url'], width=300)
                    st.write(f"**{m['titulo']}** - {m['artista']}")
                    if m.get('audio_url'): st.audio(m['audio_url'])

elif menu == "🚀 SOU ARTISTA":
    st.markdown(f"### 🚀 Distribuição Oficial King\n**Taxa:** Tu recebes {TAXA_ARTISTA}%, King {TAXA_KING}% quando plataforma pagar no PayPal **{PAYPAL_OFICIAL}**")
    titulo = st.text_input("Título *"); artista = st.text_input("Artista *"); tel = st.text_input("WhatsApp *")
    f = st.file_uploader("Música MP3 *", type=['mp3','wav','m4a']); capa = st.file_uploader("Capa 3000x3000 *", type=['jpg','jpeg','png'])
    if st.button("ENVIAR PRO KING OUVIR 👑", type="primary", use_container_width=True):
        if not titulo or not artista or not tel or not f: st.error("Preenche título, artista, WhatsApp e música!")
        else:
            isrc, upc = gen_codes()
            with st.spinner("Enviando..."):
                au = upload_file("musicas", f); cp = upload_file("capas", capa) if capa else None
            if au:
                supabase.table("musicas").insert({"titulo":titulo,"artista":artista,"tel":tel,"status":"pendente","data_envio":datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),"isrc":isrc,"upc":upc,"audio_url":au,"capa_url":cp}).execute()
                st.success(f"✅ Enviado! ISRC: {isrc}\n\nTaxa {TAXA_ARTISTA}/{TAXA_KING} | Pagamento via {PAYPAL_OFICIAL} e Moza Banco"); st.balloons()
                if cp: st.image(cp, width=200)
                st.audio(au)

elif menu == "🔐 PAINEL KING":
    s = st.text_input("Senha Dono", type="password")
    if s=="king2024":
        st.success(f"👑 King Logado - PayPal: {PAYPAL_OFICIAL}")
        pendentes = [m for m in listar() if m.get('status')=='pendente']
        st.metric("Pra ouvir", len(pendentes))
        for m in pendentes:
            with st.container(border=True):
                st.markdown(f"### {m['titulo']} - {m['artista']} | 📱 {m['tel']}")
                if m.get('capa_url'): st.image(m['capa_url'], width=200)
                if m.get('audio_url'):
                    st.markdown("🔊 **OUVE ANTES DE APROVAR:**")
                    st.audio(m['audio_url'])
                c1,c2 = st.columns(2)
                if c1.button(f"✅ APROVAR", key=f"ap{m['id']}", use_container_width=True): supabase.table("musicas").update({"status":"aprovada"}).eq("id", m['id']).execute(); st.rerun()
                if c2.button(f"❌ REJEITAR", key=f"rj{m['id']}", use_container_width=True): supabase.table("musicas").delete().eq("id", m['id']).execute(); st.rerun()
    elif s: st.error("Senha errada")

else: # BANCO
    s = st.text_input("Senha Banco King", type="password")
    if s=="king2024":
        ganhos = listar_ganhos()
        total = sum([float(g.get('valor_total',0)) for g in ganhos])
        total_king = sum([float(g.get('valor_admin',0)) for g in ganhos])
        pendente = sum([float(g.get('valor_artista',0)) for g in ganhos if g.get('status')=='pendente'])
        pago = sum([float(g.get('valor_artista',0)) for g in ganhos if g.get('status')!='pendente'])

        st.markdown(f"### 💰 BANCO OFICIAL - {PAYPAL_OFICIAL}")
        c1,c2,c3 = st.columns(3)
        c1.metric("Total Recebido", f"${total:.2f}")
        c2.metric(f"Teu Lucro {TAXA_KING}%", f"${total_king:.2f}")
        c3.metric("A Pagar", f"${pendente:.2f}")

        st.divider()
        col_pay, col_moza = st.columns(2)
        with col_pay:
            st.markdown(f"**🏦 PayPal Oficial**\n\n`{PAYPAL_OFICIAL}`")
            st.caption(f"Saldo PayPal: ${total:.2f}")
            st.link_button("Abrir PayPal", "https://paypal.com", use_container_width=True)
        with col_moza:
            st.markdown(f"**🏦 Moza Banco**\n\n`{MOZA_CONTA}`")
            st.caption(f"Para levantamentos em Meticais")
            st.link_button("Moza Banco", "https://www.mozabanco.co.mz", use_container_width=True)

        st.divider()
        st.subheader(f"➕ Spotify/YouTube te pagou no {PAYPAL_OFICIAL}? Adiciona aqui")
        with st.form("add_ganho"):
            artista_list = list(set([m['artista'] for m in listar() if m.get('status')=='aprovada']))
            if artista_list:
                artista = st.selectbox("Artista", artista_list)
            else:
                artista = st.text_input("Nome Artista")
            titulo = st.text_input("Nome Música")
            plat = st.selectbox("Plataforma que pagou", ["Spotify","YouTube","Apple Music","TikTok","Todas"])
            valor = st.number_input(f"Valor recebido em {PAYPAL_OFICIAL} ($)", min_value=0.0, step=1.0)
            tel = st.text_input("WhatsApp do artista pra pagar")
            st.info(f"Divisão automática: Artista ${valor*TAXA_ARTISTA/100:.2f} ({TAXA_ARTISTA}%) | Tu ${valor*TAXA_KING/100:.2f} ({TAXA_KING}%)")
            if st.form_submit_button("💰 LANÇAR NO BANCO"):
                v_art = valor * TAXA_ARTISTA / 100
                v_king = valor * TAXA_KING / 100
                supabase.table("ganhos").insert({"artista":artista,"titulo":titulo,"plataforma":plat,"valor_total":valor,"percent_artista":TAXA_ARTISTA,"percent_admin":TAXA_KING,"valor_artista":v_art,"valor_admin":v_king,"status":"pendente","tel_artista":tel}).execute()
                st.success(f"Lançado! {artista} vai receber ${v_art:.2f}")
                st.rerun()

        st.divider()
        st.subheader("📤 PAGAR ARTISTAS - Pendentes")
        pendentes = [g for g in ganhos if g.get('status')=='pendente']
        if not pendentes: st.info("Nenhum pagamento pendente")
        for g in pendentes:
            with st.container(border=True):
                st.markdown(f"**{g['artista']}** - {g['titulo']} | Total ${g['valor_total']} - {g['plataforma']}")
                st.markdown(f"💸 **Pagar: ${g['valor_artista']:.2f}** | Teu: ${g['valor_admin']:.2f}")
                st.write(f"📱 {g['tel_artista']}")
                cc1,cc2,cc3 = st.columns(3)
                if cc1.button("✅ Paguei Moza", key=f"mz{g['id']}", use_container_width=True):
                    supabase.table("ganhos").update({"status":"pago_moza"}).eq("id", g['id']).execute(); st.rerun()
                if cc2.button("✅ Paguei PayPal", key=f"pp{g['id']}", use_container_width=True):
                    supabase.table("ganhos").update({"status":"pago_paypal"}).eq("id", g['id']).execute(); st.rerun()
                cc3.link_button("WhatsApp", f"https://wa.me/{g['tel_artista']}?text=Ola {g['artista']}, seu repasse ${g['valor_artista']} de {g['titulo']} liberado! King Slesha - PayPal {PAYPAL_OFICIAL}", use_container_width=True)

        st.subheader("✅ Histórico Pagos")
        for g in [x for x in ganhos if x.get('status')!='pendente'][:20]:
            st.caption(f"✅ {g['artista']} - ${g['valor_artista']} - {g['status']} - {g['plataforma']} - {g['titulo']}")

    elif s:
        st.error("Senha errada")
