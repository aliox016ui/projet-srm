import streamlit as st
import pandas as pd
import json
import os
import time

LOG_FILE = "data/sms_log.json"

st.set_page_config(
    page_title="SRM-CS — Suivi SMS",
    page_icon="💧",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

.stApp { background: #f5f8ff; margin: 0; padding: 0; }

/* TOP BAR */
.top-bar {
    background: #2196C4;
    padding: 0.4rem 2rem;
    display: flex;
    gap: 2rem;
    align-items: center;
    font-size: 0.82rem;
    color: white;
}

/* HEADER */
.header {
    background: white;
    padding: 1rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 3px solid #2196C4;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}
.header-logo {
    font-size: 1.4rem;
    font-weight: 700;
    color: #2196C4;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.header-info {
    display: flex;
    gap: 2.5rem;
    align-items: center;
}
.header-info-item {
    text-align: center;
    color: #555;
    font-size: 0.82rem;
}
.header-info-item strong {
    display: block;
    color: #2196C4;
    font-size: 1rem;
}

/* NAV */
.nav-bar {
    background: #2196C4;
    padding: 0 2rem;
    display: flex;
    gap: 0;
}
.nav-item {
    color: white;
    padding: 0.9rem 1.5rem;
    font-size: 0.88rem;
    font-weight: 500;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    transition: all 0.2s;
}
.nav-item:hover, .nav-item.active {
    border-bottom: 3px solid #FF8C00;
    color: white;
}

/* LOGIN */
.login-box {
    background: white;
    padding: 3rem;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(33,150,196,0.15);
    max-width: 400px;
    margin: 4vh auto;
    border-top: 4px solid #2196C4;
}
.login-logo {
    text-align: center;
    font-size: 3rem;
    margin-bottom: 0.5rem;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%   { transform: scale(1); }
    50%  { transform: scale(1.08); }
    100% { transform: scale(1); }
}
.login-title {
    text-align: center;
    color: #2196C4;
    font-size: 1.4rem;
    font-weight: 700;
}
.login-sub {
    text-align: center;
    color: #888;
    font-size: 0.82rem;
    margin-bottom: 1.8rem;
}

/* METRICS */
.metric-card {
    background: white;
    border-radius: 12px;
    padding: 1.4rem;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
    border-top: 4px solid #2196C4;
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-3px); }
.metric-value { font-size: 2.2rem; font-weight: 700; color: #2196C4; }
.metric-label { font-size: 0.82rem; color: #888; margin-top: 0.3rem; }

/* SECTION TITLE */
.section-title {
    color: #2196C4;
    font-size: 1.1rem;
    font-weight: 700;
    border-left: 4px solid #FF8C00;
    padding-left: 0.8rem;
    margin: 1.5rem 0 1rem 0;
}

div[data-testid="stTextInput"] input {
    border-radius: 8px !important;
    border: 2px solid #e0f0fa !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #2196C4 !important;
}
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #2196C4, #1976A2) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    width: 100% !important;
}
div[data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(33,150,196,0.3) !important;
}
</style>
""", unsafe_allow_html=True)

# ─── HEADER SRM ───────────────────────────────────────────
st.markdown("""
<div class="top-bar">
    <span>✉️ contact@srm-cs.ma</span>
    <span>📞 (+212) 522 31 20 20</span>
</div>
<div class="header">
    <div class="header-logo">💧 SRM-CS</div>
    <div class="header-info">
        <div class="header-info-item">
            <span>👤 Centre de Relation Client</span>
            <strong>(+212) 522 31 20 20</strong>
        </div>
        <div class="header-info-item">
            <span>👥 Clients</span>
            <strong>+130 000</strong>
        </div>
        <div class="header-info-item">
            <span>📍 Localisation</span>
            <strong>SETTAT - MAROC</strong>
        </div>
    </div>
</div>
<div class="nav-bar">
    <div class="nav-item active">🏠 Accueil</div>
    <div class="nav-item">📊 Tableau de bord</div>
    <div class="nav-item">📨 Envois SMS</div>
    <div class="nav-item">📋 Rapports</div>
</div>
""", unsafe_allow_html=True)

# ─── SESSION STATE ────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ─── LOGIN ────────────────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div class="login-box">
            <div class="login-logo">💧</div>
            <div class="login-title">SRM-CS — Espace Interne</div>
            <div class="login-sub">Suivi des envois SMS — Accès réservé</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        username = st.text_input("👤 Utilisateur", placeholder="Identifiant")
        password = st.text_input("🔒 Mot de passe", type="password", placeholder="Mot de passe")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔐 Se connecter"):
            if username == "srm" and password == "srm2024":
                with st.spinner("Connexion en cours..."):
                    time.sleep(1)
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Identifiants incorrects")
    st.stop()

# ─── DASHBOARD ────────────────────────────────────────────
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

# ─── FILTRE DATE ──────────────────────────────────────────
st.markdown('<div class="section-title">📅 Filtrer par date</div>', unsafe_allow_html=True)
dates_dispos = sorted(df["date"].unique(), reverse=True)
date_choisie = st.selectbox(
    "Choisir un jour",
    dates_dispos,
    format_func=lambda d: d.strftime("%d/%m/%Y")
)
df = df[df["date"] == date_choisie]

total   = len(df)
pending = len(df[df["statut"] == "PENDING"])
livre   = len(df[df["statut"] == "DELIVERED"])
erreur  = len(df[df["statut"] == "ERREUR"])

# ─── METRICS ──────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Statistiques du jour</div>', unsafe_allow_html=True)
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
st.markdown('<div class="section-title">📋 Détail des envois</div>', unsafe_allow_html=True)
statuts = ["Tous"] + sorted(df["statut"].unique().tolist())
choix = st.selectbox("Filtrer par statut", statuts)
df_affiche = df if choix == "Tous" else df[df["statut"] == choix]
st.dataframe(df_affiche[["timestamp","phone","contrat","montant","statut"]], use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── CHART ────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Répartition des statuts</div>', unsafe_allow_html=True)
st.bar_chart(df["statut"].value_counts())