import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="King Slesha Distribution", page_icon=":crown:", layout="wide")

DB_MUSICAS = "musicas_db.json"
DB_USERS = "users_db.json"
FOTOS_PASTA = "fotos_perfil"
MUSICAS_PASTA = "arquivos_musicas"
CAPAS_PASTA = "capas_musicas"

for p in [FOTOS_PASTA, MUSICAS_PASTA, CAPAS_PASTA]:
    os.makedirs(p, exist_ok=True)

if not os.path.exists(DB_MUSICAS):
    with open(DB_MUSICAS, "w", encoding="utf-8") as f:
        json.dump([], f)
if not os.path.exists(DB_USERS):
    with open(DB_USERS, "w", encoding="utf-8") as f:
        json.dump([], f)

def load_musicas():
    try:
        with open(DB_MUSICAS, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_musicas(data):
    with open(DB_MUSICAS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_users():
    try:
        with open(DB_USERS, "r",
