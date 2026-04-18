import streamlit as st
import pandas as pd
import json
import os

LOG_FILE = "data/sms_log.json"

st.set_page_config(page_title="SRM-MS - Administration", page_icon="💧", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
* { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { background: white !important; }
[data-testid="stHeader"] { display: none; }
.stAlert { display: none !important; }
div[data-baseweb="notification"] { display: none !important; }

.topbar { background: #1a1a1a; color: #ccc; padding: 7px 40px; font-size: 12px; display: flex; gap: 24px; }
.navbar { background: white; border-bottom: 1.5px solid #e5e7eb; padding: 14px 40px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 999; }
.nav-brand { font-size: 15px; font-weight: 700; color: #2e7d32; display: flex; align-items: center; gap: 10px; }
.nav-circle { width: 32px; height: 32px; background: #2e7d32; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 14px; }
.nav-links { display: flex; gap: 28px; font-size: 12px; font-weight: 600; color: #444; }

.hero {
    background: linear-gradient(rgba(0,0,0,0.52), rgba(0,0,0,0.52)),
    url('https://images.unsplash.com/photo-1597212720158-ae3d645dfdb5?w=1400&q=80') center/cover no-repeat;
    padding: 90px 60px; color: white; min-height: 340px;
    display: flex; flex-direction: column; justify-content: center;
}
.hero-sub { font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: #a5d6a7; margin-bottom: 10px; }
.hero-title { font-size: 2.2rem; font-weight: 700; max-width: 620px; line-height: 1.35; }
.hero-desc { font-size: 1rem; color: rgba(255,255,255,0.78); margin-top: 12px; max-width: 480px; }

.section { padding: 50px 60px; background: #f8fafb; }
.section-title { text-align: center; font-size: 1.5rem; font-weight: 700; color: #111; margin-bottom: 6px; }
.section-sub { text-align: center; color: #6b7280; font-size: 0.9rem; margin-bottom: 32px; }

.stTextInput > label { font-weight: 600 !important; color: #374151 !important; font-size: 13px !important; }
.stTextInput > div > div > input { border: 1.5px solid #d1d5db !important; border-radius: 9px !important; padding: 11px 14px !important; font-size: 14px !important; background: #f9fafb !important; }
.stTextInput > div > div > input:focus { border-color: #2e7d32 !important; box-shadow: 0 0 0 3px rgba(46,125,50,0.12) !important; background: white !important; }

.stButton > button { background: #2e7d32 !important; color: white !important; border: none !important; border-radius: 9px !important; padding: 13px !important; font-size: 14px !important; font-weight: 600 !important; width: 100% !important; transition: all 0.25s !important; }
.stButton > button:hover { background: #1b5e20 !important; transform: translateY(-1px) !important; }

.about-section { padding: 60px; background: white; display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; }
.about-text h2 { font-size: 1.6rem; font-weight: 700; color: #111; margin-bottom: 16px; }
.about-text p { font-size: 13px; color: #555; line-height: 1.8; margin-bottom: 12px; }
.stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 28px; }
.stat-item .stat-value { font-size: 1.8rem; font-weight: 700; color: #2e7d32; }
.stat-item .stat-plus { font-size: 1.2rem; color: #2e7d32; }
.stat-item .stat-label { font-size: 12px; color: #555; margin-top: 2px; line-height: 1.4; }
.map-img { width: 100%; border-radius: 12px; }

.login-section { padding: 50px 60px; background: #f8fafb; }

.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; margin: 28px 0; }
.kpi-card { background: white; border-radius: 13px; padding: 26px 18px; text-align: center; border: 1px solid #e5e7eb; border-top: 4px solid #4caf50; }
.kpi-card.orange { border-top-color: #f59e0b; }
.kpi-card.green2 { border-top-color: #10b981; }
.kpi-card.red { border-top-color: #ef4444; }
.kpi-value { font-size: 2.2rem; font-weight: 700; color: #111; }
.kpi-label { font-size: 13px; color: #6b7280; margin-top: 5px; }

.footer { background: #1b5e20; color: white; padding: 44px 60px; }
.footer-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 40px; }
.footer-title { font-size: 13px; font-weight: 700; color: #a5d6a7; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px; }
.footer-info { font-size: 13px; line-height: 2.1; color: rgba(255,255,255,0.82); }
.footer-bottom { border-top: 1px solid rgba(255,255,255,0.15); margin-top: 32px; padding-top: 16px; font-size: 12px; color: rgba(255,255,255,0.5); text-align: center; }
.dash-section { padding: 40px 60px; background: #f8fafb; }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("""
    <div class='topbar'>
        <span>📞 Tél : 080200123</span>
        <span>✉️ service.client@srm-ms.ma</span>
    </div>
    <div class='navbar'>
        <div class='nav-brand'>
            <div class='nav-circle'>S</div>
            SRM Marrakech-Safi
        </div>
        <div class='nav-links'>
            <span>QUI SOMMES-NOUS</span>
            <span>ESPACE CLIENT</span>
            <span>CONTACT</span>
        </div>
    </div>
    <div class='hero'>
        <div class='hero-sub'>Société Régionale Multiservices — Marrakech-Safi</div>
        <div class='hero-title'>Système Automatisé de<br>Relance Client par SMS</div>
        <div class='hero-desc'>Gérez vos relances, suivez vos envois et consultez les statuts en temps réel.</div>
    </div>

    <div class='about-section'>
        <div class='about-text'>
            <h2>SRM Marrakech-Safi</h2>
            <p>Projet ambitieux et étape fondamentale dans l'évolution des services publics, la SRM-MS est entrée en fonctionnement le 1er novembre 2024.</p>
            <p>Créée en vertu de la loi n°83-21 relative aux sociétés régionales multiservices, la SRM-MS se substitue aux anciens opérateurs de distribution de la Région. Elle est dotée d'un capital de 100 millions de dirhams réparti entre ses actionnaires.</p>
            <div class='stats-grid'>
                <div class='stat-item'>
                    <span class='stat-value'>780 000</span><span class='stat-plus'> +</span>
                    <div class='stat-label'>Nombre de clients<br>Eau potable</div>
                </div>
                <div class='stat-item'>
                    <span class='stat-value'>1 470 000</span><span class='stat-plus'> +</span>
                    <div class='stat-label'>Nombre de clients<br>Electricité</div>
                </div>
                <div class='stat-item'>
                    <span class='stat-value'>394</span><span class='stat-plus'> +</span>
                    <div class='stat-label'>Complexes hydrauliques<br>Eau potable</div>
                </div>
                <div class='stat-item'>
                    <span class='stat-value'>33</span><span class='stat-plus'> +</span>
                    <div class='stat-label'>Postes sources<br>Electricité</div>
                </div>
                <div class='stat-item'>
                    <span class='stat-value'>15</span><span class='stat-plus'> +</span>
                    <div class='stat-label'>Stations d'épuration<br>Assainissement liquide</div>
                </div>
                <div class='stat-item'>
                    <span class='stat-value'>4.9</span><span class='stat-plus'> +</span>
                    <div class='stat-label'>Millions<br>Population desservie</div>
                </div>
            </div>
        </div>
        <div>
            <img class='map-img' src='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Marrakesh-Safi_region_Morocco.svg/600px-Marrakesh-Safi_region_Morocco.svg.png' />
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-section'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🔐 Espace Administration</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Connectez-vous pour accéder au tableau de bord de suivi SMS</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        username = st.text_input("Nom d'utilisateur", placeholder="Entrez votre identifiant")
        password = st.text_input("Mot de passe", type="password", placeholder="Entrez votre mot de passe")
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("Se connecter →", use_container_width=True):
            if username == "srm" and password == "srm2024":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Identifiants incorrects.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='footer'>
        <div class='footer-grid'>
            <div>
                <div class='footer-title'>Infos SRM Marrakech-Safi</div>
                <div class='footer-info'>
                    📍 Avenue Mohamed VI<br>Marrakech 40000<br>
                    📞 0524424300<br>
                    ✉️ service.client@srm-ms.ma
                </div>
            </div>
            <div>
                <div class='footer-title'>Nos Services</div>
                <div class='footer-info'>
                    Distribution eau potable<br>
                    Gestion électricité<br>
                    Assainissement liquide<br>
                    Relance client SMS
                </div>
            </div>
            <div>
                <div class='footer-title'>Liens Utiles</div>
                <div class='footer-info'>
                    Espace client<br>
                    Paiement en ligne<br>
                    Appels d'offres<br>
                    Recrutement
                </div>
            </div>
        </div>
        <div class='footer-bottom'>© 2025 SRM Marrakech-Safi — Tous droits réservés</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── DASHBOARD ──────────────────────────────────────────────────────
st.markdown("""
<div class='topbar'>
    <span>📞 Tél : 080200123</span>
    <span>✉️ service.client@srm-ms.ma</span>
</div>
<div class='navbar'>
    <div class='nav-brand'>
        <div class='nav-circle'>S</div>
        SRM Marrakech-Safi — Administration
    </div>
</div>
""", unsafe_allow_html=True)

c_sp, c_btn = st.columns([9, 1])
with c_btn:
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    if st.button("🚪 Quitter"):
        st.session_state.logged_in = False
        st.rerun()

st.markdown("<div class='dash-section'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Tableau de bord — Suivi SMS</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Suivi en temps réel des envois de relance</div>", unsafe_allow_html=True)
st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

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
    <div class='kpi-card green2'>
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
choix = st.selectbox("🔍 Filtrer par statut", statuts)
df_affiche = df if choix == "Tous" else df[df["statut"] == choix]

st.dataframe(df_affiche[["timestamp","phone","contrat","montant","statut"]], use_container_width=True, height=360)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
st.subheader("📊 Répartition des statuts")
st.bar_chart(df["statut"].value_counts())

st.markdown("""
<div class='footer' style='margin-top:40px'>
    <div class='footer-grid'>
        <div>
            <div class='footer-title'>Infos SRM</div>
            <div class='footer-info'>📍 Avenue Mohamed VI, Marrakech<br>📞 0524424300</div>
        </div>
        <div>
            <div class='footer-title'>Système SMS</div>
            <div class='footer-info'>Relance automatisée<br>des clients impayés</div>
        </div>
        <div>
            <div class='footer-title'>Support</div>
            <div class='footer-info'>service.client@srm-ms.ma<br>Lun-Ven 8h-17h</div>
        </div>
    </div>
    <div class='footer-bottom'>© 2025 SRM Marrakech-Safi</div>
</div>
""", unsafe_allow_html=True)