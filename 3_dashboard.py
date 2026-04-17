import streamlit as st
import pandas as pd
import json
import os
import time

LOG_FILE = "data/sms_log.json"

st.set_page_config(
    page_title="SRM-MS — Suivi SMS",
    page_icon="💧",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; }
.stApp { margin: 0; padding: 0; }

.srm-header {
    background: white;
    padding: 0.8rem 3rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 15px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 999;
}
.srm-logo {
    font-size: 1.5rem;
    font-weight: 800;
    color: #2196C4;
    letter-spacing: -0.5px;
}
.srm-logo span { color: #4CAF50; }
.srm-nav {
    display: flex;
    gap: 2.5rem;
    align-items: center;
}
.srm-nav a {
    color: #333;
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    transition: color 0.2s;
}
.srm-nav a:hover { color: #2196C4; }

.top-bar {
    background: #222;
    padding: 0.4rem 2rem;
    display: flex;
    gap: 2rem;
    align-items: center;
    font-size: 0.82rem;
    color: white;
}

.hero {
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
                url('https://images.unsplash.com/photo-1597212618440-806262de4f6b?w=1600&q=80');
    background-size: cover;
    background-position: center;
    min-height: 92vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}

.login-card {
    background: rgba(255,255,255,0.97);
    backdrop-filter: blur(10px);
    padding: 3rem 2.5rem;
    border-radius: 20px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.3);
    width: 100%;
    max-width: 400px;
    border-top: 5px solid #2196C4;
    animation: fadeIn 0.5s ease;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.login-logo {
    text-align: center;
    font-size: 3.5rem;
    margin-bottom: 0.5rem;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%,100% { transform: scale(1); }
    50%      { transform: scale(1.1); }
}
.login-title {
    text-align: center;
    color: #2196C4;
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}
.login-sub {
    text-align: center;
    color: #999;
    font-size: 0.8rem;
    margin-bottom: 2rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.dash-header {
    background: linear-gradient(90deg, #2196C4, #1565C0);
    padding: 1.2rem 2rem;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}
.dash-title { font-size: 1.2rem; font-weight: 700; }
.dash-sub { font-size: 0.8rem; opacity: 0.8; }

.metric-card {
    background: white;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
    border-top: 4px solid #2196C4;
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(33,150,196,0.15);
}
.metric-value { font-size: 2.5rem; font-weight: 800; color: #2196C4; }
.metric-label { font-size: 0.8rem; color: #999; margin-top: 0.3rem; text-transform: uppercase; letter-spacing: 0.5px; }

.section-title {
    font-size: 1rem;
    font-weight: 700;
    color: #1565C0;
    border-left: 4px solid #2196C4;
    padding-left: 0.8rem;
    margin: 1.5rem 0 1rem 0;
}

div[data-testid="stTextInput"] input {
    border-radius: 10px !important;
    border: 2px solid #e8f4fd !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1rem !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #2196C4 !important;
    box-shadow: 0 0 0 3px rgba(33,150,196,0.12) !important;
}
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #2196C4, #1565C0) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    padding: 0.7rem !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s !important;
}
div[data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(33,150,196,0.35) !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION ──────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ── TOP BAR + HEADER ─────────────────────────────────────
st.markdown("""
<div class="top-bar">
    <span>📞 080 200 123</span>
    <span>✉️ service.client@srm-ms.ma</span>
</div>
<div class="srm-header">
    <div class="srm-logo">💧 SRM<span>-MS</span></div>
    <div class="srm-nav">
        <a href="#">Qui sommes-nous</a>
        <a href="#">Je suis client</a>
        <a href="#">Publications</a>
        <a href="#" style="color:#2196C4;">Suivi SMS</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ── LOGIN ─────────────────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown('<div class="hero">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div class="login-card">
            <div class="login-logo">💧</div>
            <div class="login-title">SRM-MS</div>
            <div class="login-sub">Espace Interne — Suivi SMS</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        username = st.text_input("👤 Utilisateur", placeholder="Identifiant")
        password = st.text_input("🔒 Mot de passe", type="password", placeholder="Mot de passe")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔐 Se connecter"):
            if username == "srm" and password == "srm2024":
                with st.spinner("Connexion..."):
                    time.sleep(1)
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Identifiants incorrects")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ── DASHBOARD ─────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
    <div>
        <div class="dash-title">📊 Tableau de bord — Suivi SMS</div>
        <div class="dash-sub">Société Régionale Multiservices Marrakech-Safi</div>
    </div>
</div>
""", unsafe_allow_html=True)

col_space, col_logout = st.columns([6, 1])
with col_logout:
    if st.button("🚪 Déconnexion"):
        st.session_state.logged_in = False
        st.rerun()

# ── DATA ──────────────────────────────────────────────────
if not os.path.exists(LOG_FILE):
    st.info("📭 Aucun SMS envoyé pour le moment.")
    st.stop()

with open(LOG_FILE, "r", encoding="utf-8") as f:
    log = json.load(f)

df = pd.DataFrame(log)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date

# ── FILTRE DATE ───────────────────────────────────────────
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

# ── METRICS ───────────────────────────────────────────────
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

# ── TABLE ─────────────────────────────────────────────────
st.markdown('<div class="section-title">📋 Détail des envois</div>', unsafe_allow_html=True)
statuts = ["Tous"] + sorted(df["statut"].unique().tolist())
choix = st.selectbox("Filtrer par statut", statuts)
df_affiche = df if choix == "Tous" else df[df["statut"] == choix]
st.dataframe(df_affiche[["timestamp","phone","contrat","montant","statut"]], use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── CHART ─────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Répartition des statuts</div>', unsafe_allow_html=True)
st.bar_chart(df["statut"].value_counts())