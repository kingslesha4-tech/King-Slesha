import streamlit as st
import datetime
import random
import pandas as pd
import time

PAYPAL_OFICIAL = 'Kingslesha4@gmail.com'
SENHA_KING = 'chila1990'

if 'musicas' not in st.session_state:
    st.session_state['musicas'] = []
if 'logado' not in st.session_state:
    st.session_state['logado'] = False

st.set_page_config(page_title='King Slesha Moz', page_icon='KING')
st.markdown("<h1 style='background:black;color:gold;text-align:center;padding:20px;border-radius:10px;'>KING SLESHA MOZ - DISTRIBUIDORA</h1>", unsafe_allow_html=True)

menu = st.sidebar.selectbox('Menu', ['Enviar Musica', 'Painel King'])

if menu == 'Enviar Musica':
    st.subheader('Enviar Musica')
    nome = st.text_input('Nome Artista *')
    email_a = st.text_input('Email Artista *')
    titulo = st.text_input('Titulo Musica *')
    # GENERO COM KIZOMBA DE VOLTA - TUA COISA
    genero = st.selectbox('Genero', ['Amapiano', 'Afrobeat', 'Hip Hop', 'Marrabenta', 'Pandza', 'Kizomba', 'Zouk', 'Afro House', 'R&B', 'Outro'])

    st.write('---')
    st.subheader('Forma de Receber 70%')
    forma_pag = st.selectbox('Escolhe como quer receber', ['PayPal', 'M-Pesa', 'e-Mola', 'Conta Bancaria'])

    paypal_a = ''
    mpesa_num = ''
    emola_num = ''
    banco_nome = ''
    banco_conta = ''
    banco_nib = ''

    if forma_pag == 'PayPal':
        paypal_a = st.text_input('Seu PayPal 70% *', placeholder='seu@gmail.com')
    if forma_pag == 'M-Pesa':
        mpesa_num = st.text_input('Seu Numero M-Pesa *', placeholder='84xxxxxxx')
    if forma_pag == 'e-Mola':
        emola_num = st.text_input('Seu Numero e-Mola *', placeholder='82xxxxxxx')
    if forma_pag == 'Conta Bancaria':
        banco_nome = st.selectbox('Banco', ['BCI', 'Millennium BIM', 'Standard Bank', 'Moza Banco', 'ABSA', 'Outro'])
        banco_conta = st.text_input('Numero da Conta *')
        banco_nib = st.text_input('NIB *', placeholder='0000...')

    st.write('---')
    mp3 = st.file_uploader('MP3/WAV/M4A *', type=['mp3','wav','m4a'])
    capa = st.file_uploader('Capa 3000x3000 *', type=['jpg','png','jpeg'])
    ok = st.checkbox('Aceito contrato 70/30')

    if st.button('ENVIAR PARA KING', use_container_width=True, type='primary'):
        if not ok or not nome or not titulo or not mp3:
            st.error('Preenche tudo!')
        else:
            texto = st.empty()
            barra = st.progress(0)
            texto.write('Iniciando envio 0%')
            barra.progress(10)
            time.sleep(0.3)
            texto.write('Salvando MP3 30%')
            barra.progress(30)
            time.sleep(0.3)
            texto.write('Salvando capa 60%')
            barra.progress(60)
            time.sleep(0.3)
            texto.write('Gerando ISRC 85%')
            barra.progress(85)
            time.sleep(0.3)

            isrc = 'MZ-KSM-25-' + str(random.randint(10000,99999))
            mp3_data = mp3.getvalue()
            capa_data = capa.getvalue() if capa else None

            nova = {
                'Data': datetime.datetime.now().strftime('%d/%m/%Y %H:%M'),
                'Artista': nome,
                'Musica': titulo,
                'Genero': genero,
                'Email': email_a,
                'Forma Pag': forma_pag,
                'PayPal Artista': paypal_a,
                'M-Pesa': mpesa_num,
                'e-Mola': emola_num,
                'Banco': banco_nome,
                'Conta': banco_conta,
                'NIB': banco_nib,
                'ISRC': isrc,
                'Status': 'Pendente',
                'mp3_bytes': mp3_data,
                'mp3_nome': mp3.name,
                'capa_bytes': capa_data,
                'capa_nome': capa.name if capa else None
            }
            st.session_state['musicas'].append(nova)
            barra.progress(100)
            texto.write('Concluido 100% - Musica terminou!')
            st.success('Recebido! ISRC ' + isrc)
            st.balloons()

else:
    st.subheader('Painel King Slesha')
    if not st.session_state['logado']:
        senha = st.text_input('Senha King', type='password', placeholder='Digite sua senha')
        if st.button('ENTRAR NO PAINEL', use_container_width=True, type='primary'):
            if senha.lower().strip() == SENHA_KING:
                st.session_state['logado'] = True
                st.rerun()
            else:
                st.error('Senha incorreta!')
    else:
        st.success('Bem-vindo King!')
        col1, col2, col3 = st.columns(3)
        total = len(st.session_state['musicas'])
        pendentes = 0
        for mm in st.session_state['musicas']:
            if mm['Status'] == 'Pendente':
                pendentes = pendentes + 1
        col1.metric('Total Musicas', total)
        col2.metric('Pendentes', pendentes)
        col3.metric('Status', 'Online')
        col4, col5 = st.columns(2)
        col4.metric('PayPal Oficial', PAYPAL_OFICIAL)
        col5.metric('Divisao', '70/30')

        st.write('---')
        st.subheader('Musicas para Ouvir, Baixar e Aprovar')

        if total == 0:
            st.info('Nenhuma musica ainda.')
        else:
            df = pd.DataFrame([{k:v for k,v in m.items() if k not in ['mp3_bytes','capa_bytes']} for m in st.session_state['musicas']])
            st.dataframe(df, use_container_width=True)
            st.write('---')
            for i in range(len(st.session_state['musicas'])):
                m = st.session_state['musicas'][i]
                artista = m['Artista']
                musica = m['Musica']
                status = m['Status']
                forma = m['Forma Pag']
                genero_m = m.get('Genero', 'N/A')
                titulo_exp = 'MUSICA ' + artista + ' - ' + musica + ' - ' + status
                with st.expander(titulo_exp):
                    st.write('Artista: ' + artista + ' | Genero: ' + genero_m)
                    st.write('Email: ' + m['Email'] + ' | Forma: ' + forma)
                    st.write('ISRC: ' + m['ISRC'] + ' | Data: ' + m['Data'])

                    # PARTE DA MUSICA E CAPA - AGORA SEMPRE MOSTRA OS 2
                    st.write('---')
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write('**MUSICA PARA OUVIR E BAIXAR**')
                        if m.get('mp3_bytes') and m['mp3_bytes'] is not None:
                            try:
                                if len(m['mp3_bytes']) > 100:
                                    st.audio(m['mp3_bytes'], format='audio/mp3')
                                    k1 = 'mp3_' + str(i)
                                    st.download_button('BAIXAR MUSICA', m['mp3_bytes'], file_name=m['mp3_nome'], key=k1, use_container_width=True)
                                else:
                                    st.warning('MP3 muito pequeno - reenvie')
                            except:
                                st.error('Erro no MP3')
                        else:
                            st.error('Musica nao encontrada - artista precisa reenviar')

                    with col_b:
                        st.write('**CAPA**')
                        if m.get('capa_bytes') and m['capa_bytes'] is not None:
                            st.image(m['capa_bytes'], width=250)
                            k2 = 'capa_' + str(i)
                            st.download_button('BAIXAR CAPA', m['capa_bytes'], file_name=m['capa_nome'], key=k2, use_container_width=True)
                        else:
                            st.warning('Sem capa')

                    st.write('---')
                    if status == 'Pendente':
                        k3 = 'aprov_' + str(i)
                        if st.button('APROVAR ESTA MUSICA', key=k3, type='primary', use_container_width=True):
                            st.session_state['musicas'][i]['Status'] = 'Aprovada'
                            st.rerun()
                    else:
                        st.success('Ja Aprovada')

        if st.button('SAIR'):
            st.session_state['logado'] = False
            st.rerun()
