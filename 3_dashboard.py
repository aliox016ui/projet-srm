import streamlit as st
import pandas as pd
import json
import os

LOG_FILE = "data/sms_log.json"

st.set_page_config(page_title="SRM - Suivi SMS", page_icon="💧", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; }

/* ── LOGIN PAGE ── */
.login-wrapper {
    min-height: 100vh;
    background: linear-gradient(135deg, #0a2540 0%, #1a5276 50%, #2196C4 100%);
    display: flex;
    align-items: center;
    justify-content: center;
}
.login-box {
    background: white;
    border-radius: 20px;
    padding: 50px 44px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    max-width: 420px;
    width: 100%;
}
.login-header {
    text-align: center;
    margin-bottom: 32px;
}
.login-icon {
    font-size: 3rem;
    margin-bottom: 8px;
}
.login-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #0a2540;
    margin: 0;
}
.login-sub {
    color: #6b7280;
    font-size: 0.9rem;
    margin-top: 4px;
}
.divider-line {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 24px 0;
}

/* ── INPUTS ── */
.stTextInput > label {
    font-weight: 600 !important;
    color: #374151 !important;
    font-size: 0.85rem !important;
}
.stTextInput > div > div > input {
    border: 2px solid #e5e7eb !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
    font-size: 0.95rem !important;
    background: #f9fafb !important;
    transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #2196C4 !important;
    background: white !important;
    box-shadow: 0 0 0 3px rgba(33,150,196,0.15) !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #2196C4, #0a2540) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: all 0.3s !important;
    letter-spacing: 0.5px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(33,150,196,0.4) !important;
}

/* ── DASHBOARD ── */
.dash-header {
    background: linear-gradient(135deg, #0a2540, #2196C4);
    padding: 20px 32px;
    color: white;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 32px;
}
.dash-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: white;
}
.dash-sub {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.75);
}
.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 24px 20px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.08);
    text-align: center;
    border-top: 4px solid #2196C4;
}
.kpi-value {
    font-size: 2.2rem;
    font-weight: 700;
    color: #0a2540;
}
.kpi-label {
    font-size: 0.85rem;
    color: #6b7280;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

# ── AUTH ───────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    c1, c2, c3 = st.columns([1, 1.4, 1])
    with c2:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div class='login-header'>
                <div class='login-icon'>💧</div>
                <div class='login-title'>SRM — Marrakech Safi</div>
                <div class='login-sub'>Système de Relance SMS</div>
            </div>
            <hr class='divider-line'>
        """, unsafe_allow_html=True)

        username = st.text_input("Nom d'utilisateur", placeholder="Entrez votre identifiant")
        password = st.text_input("Mot de passe", type="password", placeholder="Entrez votre mot de passe")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("Se connecter →", use_container_width=True):
            if username == "srm" and password == "srm2024":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Identifiants incorrects. Veuillez réessayer.")
    st.stop()

# ── DASHBOARD ──────────────────────────────────────────────────────
st.markdown("""
    <div class='dash-header'>
        <div>
            <div class='dash-title'>💧 SRM — Tableau de bord SMS</div>
            <div class='dash-sub'>Suivi en temps réel des envois</div>
        </div>
    </div>
""", unsafe_allow_html=True)

col_space, col_btn = st.columns([8, 1])
with col_btn:
    if st.button("🚪 Quitter"):
        st.session_state.logged_in = False
        st.rerun()

if not os.path.exists(LOG_FILE):
    st.info("📭 Aucun SMS envoyé pour le moment.")
    st.stop()

with open(LOG_FILE, "r", encoding="utf-8") as f:
    log = json.load(f)

df = pd.DataFrame(log)

total   = len(df)
pending = len(df[df["statut"] == "PENDING"])
livre   = len(df[df["statut"] == "DELIVERED"])
erreur  = len(df[df["statut"] == "ERREUR"])

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"<div class='kpi-card'><div class='kpi-value'>{total}</div><div class='kpi-label'>📨 Total SMS</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='kpi-card' style='border-color:#f59e0b'><div class='kpi-value' style='color:#f59e0b'>{pending}</div><div class='kpi-label'>⏳ En cours</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='kpi-card' style='border-color:#10b981'><div class='kpi-value' style='color:#10b981'>{livre}</div><div class='kpi-label'>✅ Livrés</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='kpi-card' style='border-color:#ef4444'><div class='kpi-value' style='color:#ef4444'>{erreur}</div><div class='kpi-label'>❌ Erreurs</div></div>", unsafe_allow_html=True)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
st.divider()

statuts = ["Tous"] + sorted(df["statut"].unique().tolist())
choix   = st.selectbox("🔍 Filtrer par statut", statuts)
df_affiche = df if choix == "Tous" else df[df["statut"] == choix]

st.dataframe(
    df_affiche[["timestamp", "phone", "contrat", "montant", "statut"]],
    use_container_width=True,
    height=350
)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
st.subheader("📊 Répartition des statuts")
st.bar_chart(df["statut"].value_counts())