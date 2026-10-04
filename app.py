import streamlit as st, os, datetime, random, string
from supabase import create_client

# --- CONFIG QUE NUNCA APAGA ---
SUPABASE_URL = "https://SEU_PROJETO.supabase.co"
SUPABASE_KEY = "SUA_KEY_AQUI"
# Cria conta grátis em supabase.com > New Project > copia URL e KEY

@st.cache_resource
def get_supabase():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except:
        return None

supabase = get_supabase()

st.set_page_config(page_title="KING SLESHA MOZ - V8 NUNCA APAGA", page_icon="👑", layout="centered")

st.markdown("""
<div style="text-align:center; background:black; padding:20px; border-radius:15px; border:2px solid #1DB954;">
<h1 style="color:#1DB954;">👑 KING SLESHA MOZ V8</h1>
<p style="color:white;">AGORA COM BANCO QUE NUNCA APAGA!</p>
</div>
""", unsafe_allow_html=True)

# ... resto igual mas salvando no supabase ...
# Se supabase falhar, salva local tb
