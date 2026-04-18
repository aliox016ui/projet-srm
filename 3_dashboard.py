import streamlit as st
import pandas as pd
import json
import os

LOG_FILE = "data/sms_log.json"

st.set_page_config(page_title="SRM-MS - Suivi SMS", page_icon="💧", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

* { font-family: 'Inter', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── TOP BAR ── */
.top-bar {
    background: #1a1a1a;
    color: white;
    padding: 8px 40px;
    font-size: 0.8rem;
    display: flex;
    gap: 24px;
}

/* ── NAVBAR ── */
.navbar {
    background: white;
    padding: 16px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    position: sticky;
    top: 0;
    z-index: 999;
}
.nav-logo {
    font-size: 1.3rem;
    font-weight: 700;
    color: #2e7d32;
}
.nav-links {
    display: flex;
    gap: 32px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #333;
}

/* ── HERO ── */
.hero {
    background: linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.45)),
                url('https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Jardin_Majorelle_Marrakech.jpg/1280px-Jardin_Majorelle_Marrakech.jpg');
    background-size: cover;
    background-position: center;
    padding: 100px 60px;
    color: white;
    min-height: 420px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.hero-sub {
    font-size: 0.9rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 12px;
    color: #a5d6a7;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    max-width: 700px;
    line-height: 1.3;
}

/* ── SECTION ── */
.section {
    padding: 60px 60px;
}
.section-title {
    text-align: center;
    font-size: 1.6rem;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 8px;
}
.section-sub {
    text-align: center;
    color: #6b7280;
    font-size: 0.9rem;
    margin-bottom: 40px;
}

/* ── KPI CARDS ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 40px;
}
.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 28px 20px;
    text-align: center;
    box-shadow: 0 2px 16px rgba(0,0,0,0.08);
    border-top: 4px solid #4caf50;
}
.kpi-card.orange { border-top-color: #f59e0b; }
.kpi-card.green  { border-top-color: #10b981; }
.kpi-card.red    { border-top-color: #ef4444; }
.kpi-value {
    font-size: 2.4rem;
    font-weight: 700;
    color: #1a1a1a;
}
.kpi-label {
    font-size: 0.85rem;
    color: #6b7280;
    margin-top: 6px;
}

/* ── LOGIN ── */
.login-card {
    background: white;
    border-radius: 16px;
    padding: 48px 40px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.12);
    max-width: 420px;
    margin: 0 auto;
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
    background: #f9fafb !important;
}
.stTextInput > div > div > input:focus {
    border-color: #4caf50 !important;
    box-shadow: 0 0 0 3px rgba(76,175,80,0.15) !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: #4caf50 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    background: #388e3c !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(76,175,80,0.35) !important;
}

/* ── FOOTER ── */
.footer {
    background: #2e7d32;
    color: white;
    padding: 40px 60px;
    margin-top: 60px;
}
.footer-title {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 16px;
    color: #a5d6a7;
}
.footer-info {
    font-size: 0.85rem;
    line-height: 2;
    color: rgba(255,255,255,0.85);
}
</style>
""", unsafe_allow_html=True)

# ── AUTH ───────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # TOP BAR
    st.markdown("""
    <div class='top-bar'>
        <span>📞 Call : 080200123</span>
        <span>✉️ service.client@srm-ms.ma</span>
    </div>
    <div class='navbar'>
        <div class='nav-logo'>💧 SRM Marrakech-Safi</div>
        <div class='nav-links'>
            <span>QUI SOMMES-NOUS?</span>
            <span>SYSTEME SMS</span>
            <span>CONTACT</span>
        </div>
    </div>
    <div class='hero'>
        <div class='hero-sub'>Société Régionale Multiservices — Marrakech-Safi</div>
        <div class='hero-title'>Système Automatisé de<br>Relance Client par SMS</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.4, 1])
    with c2:
        st.markdown("<div class='section-title'>🔐 Espace Administration</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-sub'>Connectez-vous pour accéder au tableau de bord</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        username = st.text_input("Nom d'utilisateur", placeholder="Identifiant")
        password = st.text_input("Mot de passe", type="password", placeholder="Mot de passe")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("Se connecter →", use_container_width=True):
            if username == "srm" and password == "srm2024":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Identifiants incorrects.")

    # FOOTER
    st.markdown("""
    <div class='footer'>
        <div style='display:grid;grid-template-columns:1fr 1fr;gap:40px'>
            <div>
                <div class='footer-title'>Infos SRM Marrakech-Safi</div>
                <div class='footer-info'>
                    📍 Siège : Avenue Mohamed VI, Marrakech 40000<br>
                    📞 Mobile : 0524424300<br>
                    ✉️ service.client@srm-ms.ma
                </div>
            </div>
            <div>
                <div class='footer-title'>À propos</div>
                <div class='footer-info'>
                    SRM Marrakech-Safi assure la distribution<br>
                    d'eau potable, d'électricité et la gestion<br>
                    de l'assainissement liquide.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── DASHBOARD ──────────────────────────────────────────────────────
st.markdown("""
<div class='top-bar'>
    <span>📞 Call : 080200123</span>
    <span>✉️ service.client@srm-ms.ma</span>
</div>
<div class='navbar'>
    <div class='nav-logo'>💧 SRM Marrakech-Safi</div>
    <div class='nav-links'>
        <span>TABLEAU DE BORD SMS</span>
    </div>
</div>
""", unsafe_allow_html=True)

col_sp, col_btn = st.columns([8, 1])
with col_btn:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("🚪 Quitter"):
        st.session_state.logged_in = False
        st.rerun()

st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Tableau de bord — Suivi SMS</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Suivi en temps réel des envois de relance</div>", unsafe_allow_html=True)
st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

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

st.markdown(f"""
<div class='kpi-grid'>
    <div class='kpi-card'>
        <div class='kpi-value'>{total}</div>
        <div class='kpi-label'>📨 Total SMS</div>
    </div>
    <div class='kpi-card orange'>
        <div class='kpi-value' style='color:#f59e0b'>{pending}</div>
        <div class='kpi-label'>⏳ En cours</div>
    </div>
    <div class='kpi-card green'>
        <div class='kpi-value' style='color:#10b981'>{livre}</div>
        <div class='kpi-label'>✅ Livrés</div>
    </div>
    <div class='kpi-card red'>
        <div class='kpi-value' style='color:#ef4444'>{erreur}</div>
        <div class='kpi-label'>❌ Erreurs</div>
    </div>
</div>
""", unsafe_allow_html=True)

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

st.markdown("""
<div class='footer'>
    <div style='display:grid;grid-template-columns:1fr 1fr;gap:40px'>
        <div>
            <div class='footer-title'>Infos SRM Marrakech-Safi</div>
            <div class='footer-info'>
                📍 Avenue Mohamed VI, Marrakech 40000<br>
                📞 0524424300<br>
                ✉️ service.client@srm-ms.ma
            </div>
        </div>
        <div>
            <div class='footer-title'>Système SMS</div>
            <div class='footer-info'>
                Relance automatisée des clients<br>
                ayant des factures impayées.
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)