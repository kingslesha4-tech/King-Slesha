import streamlit as st
import datetime
import random
import pandas as pd
import time

PAYPAL_OFICIAL = 'Kingslesha4@gmail.com'
SENHA_KING = 'chila1990'
EMAIL_KING = 'kingslesha4@gmail.com'

if 'musicas' not in st.session_state:
    st.session_state['musicas'] = []
if 'pagamentos' not in st.session_state:
    st.session_state['pagamentos'] = []
if 'users' not in st.session_state:
    st.session_state['users'] = []
if 'logado' not in st.session_state:
    st.session_state['logado'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None
if 'is_king' not in st.session_state:
    st.session_state['is_king'] = False

st.set_page_config(page_title='King Slesha Moz', page_icon='KING')
st.markdown("<h1 style='background:black;color:gold;text-align:center;padding:20px;border-radius:10px;'>KING SLESHA MOZ - DISTRIBUIDORA</h1>", unsafe_allow_html=True)

# FUNCAO PARA REGISTAR
def registar_user(nome, email, senha):
    for u in st.session_state['users']:
        if u['email'].lower() == email.lower():
            return False
    st.session_state['users'].append({'nome': nome, 'email': email.lower(), 'senha': senha, 'data': datetime.datetime.now().strftime('%d/%m/%Y')})
    return True

def login_user(email, senha):
    # King entra
    if email.lower() == EMAIL_KING.lower() and senha == SENHA_KING:
        st.session_state['is_king'] = True
        st.session_state['logado'] = True
        st.session_state['current_user'] = {'nome': 'King Slesha', 'email': email}
        return True
    for u in st.session_state['users']:
        if u['email'].lower() == email.lower() and u['senha'] == senha:
            st.session_state['current_user'] = u
            st.session_state['is_king'] = False
            st.session_state['logado'] = True
            return True
    return False

# MENU DINAMICO
if not st.session_state['logado']:
    menu = st.sidebar.selectbox('Menu', ['Login', 'Registar', 'Painel King'])
else:
    if st.session_state['is_king']:
        menu = st.sidebar.selectbox('Menu King', ['Painel King', 'Sair'])
    else:
        menu = st.sidebar.selectbox('Menu Artista', ['Enviar Musica', 'Minhas Musicas', 'Sair'])
        st.sidebar.success('Logado: ' + st.session_state['current_user']['nome'])

# TELA DE REGISTAR
if menu == 'Registar' and not st.session_state['logado']:
    st.subheader('Criar Conta - Artista')
    st.write('Cada cliente cria sua propria conta para entrar na plataforma')

    nome_r = st.text_input('Nome Completo *', key='reg_nome')
    email_r = st.text_input('Email *', placeholder='seu@gmail.com', key='reg_email')
    senha_r = st.text_input('Senha *', type='password', key='reg_senha')
    senha_r2 = st.text_input('Confirmar Senha *', type='password', key='reg_senha2')

    st.write('---')
    if st.button('CRIAR CONTA', type='primary', use_container_width=True):
        if not nome_r or not email_r or not senha_r:
            st.error('Preenche tudo!')
        elif senha_r!= senha_r2:
            st.error('Senhas diferentes!')
        elif len(senha_r) < 4:
            st.error('Senha minimo 4 caracteres!')
        else:
            if registar_user(nome_r, email_r, senha_r):
                st.success('Conta criada com sucesso! Agora faz Login!')
                st.balloons()
                time.sleep(1)
                st.rerun()
            else:
                st.error('Email ja existe! Faz Login')

    st.write('---')
    st.write('**Ou**')
    if st.button('Continuar com Google', use_container_width=True):
        st.info('Para ativar Google Login de verdade, depois eu te ajudo a configurar com Firebase. Por enquanto cria conta com Email acima - funciona igual!')
        # Simula login google
        email_g = st.text_input('Coloca seu Gmail do Google', placeholder='seu@gmail.com', key='google_email')
        if st.button('Entrar com este Gmail'):
            if email_g:
                # Cria conta automatica google
                if registar_user(email_g.split('@')[0], email_g, 'google123'):
                    login_user(email_g, 'google123')
                    st.success('Entrou com Google: ' + email_g)
                    st.rerun()
                else:
                    login_user(email_g, 'google123')
                    st.rerun()

    st.write('Ja tem conta? Vai em Login no menu lateral')

# TELA DE LOGIN
if menu == 'Login' and not st.session_state['logado']:
    st.subheader('Entrar na Plataforma')
    email_l = st.text_input('Email *', placeholder='seu@gmail.com', key='login_email')
    senha_l = st.text_input('Senha *', type='password', key='login_senha')

    if st.button('ENTRAR', type='primary', use_container_width=True):
        if login_user(email_l, senha_l):
            st.success('Bem-vindo!')
            st.rerun()
        else:
            st.error('Email ou senha errada! Se nao tem conta, vai em Registar')

    st.write('---')
    st.write('**Ou entra com:**')
    if st.button('Entrar com Google', key='login_google', use_container_width=True):
        st.session_state['show_google_login'] = True

    if st.session_state.get('show_google_login', False):
        email_g = st.text_input('Seu Gmail', key='g_login')
        if st.button('Confirmar Google Login'):
            # Se ja existe, loga, se nao cria
            existe = False
            for u in st.session_state['users']:
                if u['email'].lower() == email_g.lower():
                    existe = True
                    st.session_state['current_user'] = u
                    st.session_state['logado'] = True
                    st.session_state['is_king'] = False
                    st.rerun()
            if not existe and email_g:
                registar_user(email_g.split('@')[0], email_g, 'google123')
                login_user(email_g, 'google123')
                st.rerun()

    st.info('Nao tem conta? Clica em Registar no menu lateral')

# ENVIAR MUSICA - SO SE LOGADO COMO ARTISTA
if menu == 'Enviar Musica' and st.session_state['logado'] and not st.session_state['is_king']:
    st.subheader('Enviar Musica - Log
