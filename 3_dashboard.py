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

.login-container {
    max-width: 420px;
    margin: 80px auto;
    background: white;
    border-radius: 16px;
    padding: 48px 40px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.12);
}

.login-logo {
    text-align: center;
    margin-bottom: 8px;
    font-size: 2.5rem;
}

.login-title {
    text-align: center;
    font-size: 1.5rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 4px;
}

.login-subtitle {
    text-align: center;
    color: #6b7280;
    font-size: 0.9rem;
    margin-bottom: 32px;
}

.stTextInput > div > div > input {
    border: 2px solid #e5e7eb !important;
    border-radius: 10px !important;
    padding: 12px 16px !important;
    font-size: 0.95rem !important;
    transition: border-color 0.2s !important;
}

.stTextInput > div > div > input:focus {
    border-color: #2196C4 !important;
    box-shadow: 0 0 0 3px rgba(33,150,196,0.1) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #2196C4, #1a7a9e) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(33,150,196,0.4) !important;
}

.metric-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border-left: 4px solid #2196C4;
}
</style>
""", unsafe_allow_html=True)

# ── Authentication ─────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="login-logo">💧</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-title">SRM — Marrakech Safi</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Système de Relance SMS</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">────────────────────</div>', unsafe_allow_html=True)

        username = st.text_input("Nom d'utilisateur", placeholder="Entrez votre identifiant")
        password = st.text_input("Mot de passe", type="password", placeholder="Entrez votre mot de passe")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Se connecter →", use_container_width=True):
            if username == "srm" and password == "srm2024":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Identifiants incorrects")
    st.stop()

# ── Dashboard ──────────────────────────────────────────────────────
col_title, col_btn = st.columns([6, 1])
with col_title:
    st.markdown("## 💧 SRM — Tableau de bord SMS")
with col_btn:
    if st.button("🚪 Déconnexion"):
        st.session_state.logged_in = False
        st.rerun()

st.divider()

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

col1, col2, col3, col4 = st.columns(4)
col1.metric("📨 Total", total)
col2.metric("⏳ En cours", pending)
col3.metric("✅ Livrés", livre)
col4.metric("❌ Erreurs", erreur)

st.divider()

statuts = ["Tous"] + sorted(df["statut"].unique().tolist())
choix   = st.selectbox("Filtrer par statut", statuts)

df_affiche = df if choix == "Tous" else df[df["statut"] == choix]

st.dataframe(
    df_affiche[["timestamp", "phone", "contrat", "montant", "statut"]],
    use_container_width=True
)

st.subheader("Répartition des statuts")
st.bar_chart(df["statut"].value_counts())
