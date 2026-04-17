import streamlit as st
import pandas as pd
import json
import os
import time

# ─── CONFIG ───────────────────────────────────────────────
LOG_FILE = "data/sms_log.json"

st.set_page_config(
    page_title="SRM - Suivi SMS",
    page_icon="💧",
    layout="wide"
)

# ─── CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp { background: linear-gradient(135deg, #f0f4ff 0%, #e8f0fe 100%); }

.login-box {
    background: white;
    padding: 3rem;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0,82,204,0.15);
    max-width: 420px;
    margin: 5vh auto;
    border-top: 5px solid #0052CC;
}

.logo-circle {
    width: 80px; height: 80px;
    background: linear-gradient(135deg, #0052CC, #0079FF);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 1rem auto;
    font-size: 2rem;
    box-shadow: 0 8px 25px rgba(0,82,204,0.3);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%   { box-shadow: 0 0 0 0 rgba(0,82,204,0.4); }
    70%  { box-shadow: 0 0 0 15px rgba(0,82,204,0); }
    100% { box-shadow: 0 0 0 0 rgba(0,82,204,0); }
}

.login-title {
    text-align: center;
    color: #0052CC;
    font-size: 1.6rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}

.login-sub {
    text-align: center;
    color: #888;
    font-size: 0.85rem;
    margin-bottom: 2rem;
}

.metric-card {
    background: white;
    border-radius: 15px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,82,204,0.08);
    border-left: 5px solid #0052CC;
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-3px); }

.metric-value { font-size: 2.5rem; font-weight: 700; color: #0052CC; }
.metric-label { font-size: 0.85rem; color: #888; margin-top: 0.3rem; }

.header-bar {
    background: linear-gradient(90deg, #0052CC, #0079FF);
    padding: 1rem 2rem;
    border-radius: 15px;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 20px rgba(0,82,204,0.2);
}

div[data-testid="stTextInput"] input {
    border-radius: 10px !important;
    border: 2px solid #e0e7ff !important;
    padding: 0.6rem 1rem !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #0052CC !important;
    box-shadow: 0 0 0 3px rgba(0,82,204,0.1) !important;
}

div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #0052CC, #0079FF) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: all 0.3s !important;
}
div[data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0,82,204,0.3) !important;
}
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ─── LOGIN PAGE ───────────────────────────────────────────
if not st.session_state.logged_in:

    st.markdown("""
    <div class="login-box">
        <div class="logo-circle">💧</div>
        <div class="login-title">SRM — Suivi SMS</div>
        <div class="login-sub">Société de la Régionale des Eaux</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        username = st.text_input("👤 Utilisateur", placeholder="Entrez votre identifiant")
        password = st.text_input("🔒 Mot de passe", type="password", placeholder="Entrez votre mot de passe")
        st.markdown("<br>", unsafe_allow_html=True)
        login_btn = st.button("Se connecter")

        if login_btn:
            if username == "srm" and password == "srm2024":
                with st.spinner("Connexion en cours..."):
                    time.sleep(1)
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Identifiants incorrects")

    st.stop()

# ─── DASHBOARD ────────────────────────────────────────────
st.markdown("""
<div class="header-bar">
    <div style="font-size:1.3rem; font-weight:700;">💧 SRM — Tableau de bord SMS</div>
    <div style="font-size:0.85rem; opacity:0.85;">Société de la Régionale des Eaux</div>
</div>
""", unsafe_allow_html=True)

# Logout
col_space, col_logout = st.columns([6, 1])
with col_logout:
    if st.button("🚪 Déconnexion"):
        st.session_state.logged_in = False
        st.rerun()

# ─── DATA ─────────────────────────────────────────────────
if not os.path.exists(LOG_FILE):
    st.info("📭 Aucun SMS envoyé pour le moment.")
    st.stop()

with open(LOG_FILE, "r", encoding="utf-8") as f:
    log = json.load(f)

df = pd.DataFrame(log)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date

# ─── FILTRE PAR DATE ──────────────────────────────────────
st.markdown("### 📅 Filtrer par date")
dates_dispos = sorted(df["date"].unique(), reverse=True)
date_choisie = st.selectbox(
    "Choisir un jour",
    dates_dispos,
    format_func=lambda d: d.strftime("%d/%m/%Y")
)

df = df[df["date"] == date_choisie]

# ─── METRICS ──────────────────────────────────────────────
total   = len(df)
pending = len(df[df["statut"] == "PENDING"])
livre   = len(df[df["statut"] == "DELIVERED"])
erreur  = len(df[df["statut"] == "ERREUR"])

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{total}</div><div class="metric-label">📨 Total envoyés</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#F59E0B;">{pending}</div><div class="metric-label">⏳ En cours</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#10B981;">{livre}</div><div class="metric-label">✅ Livrés</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#EF4444;">{erreur}</div><div class="metric-label">❌ Erreurs</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── TABLE ────────────────────────────────────────────────
st.markdown("### 📋 Détail des envois")
statuts = ["Tous"] + sorted(df["statut"].unique().tolist())
choix = st.selectbox("Filtrer par statut", statuts)
df_affiche = df if choix == "Tous" else df[df["statut"] == choix]
st.dataframe(df_affiche[["timestamp","phone","contrat","montant","statut"]], use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── CHART ────────────────────────────────────────────────
st.markdown("### 📊 Répartition des statuts")
st.bar_chart(df["statut"].value_counts())