import streamlit as st
import pandas as pd
import os
import re
from supabase import create_client

# ── CONFIG ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SRM-MS — Suivi SMS",
    page_icon="https://www.srm-ms.ma/wp-content/uploads/2024/10/cropped-favicon-srm-32x32.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── SUPABASE ──────────────────────────────────────────────────────
def get_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if url and key:
        return create_client(url, key)
    return None

def load_data():
    supabase = get_supabase()
    if supabase:
        resp = supabase.table("sms_log").select("*").order("timestamp", desc=True).execute()
        return pd.DataFrame(resp.data) if resp.data else pd.DataFrame()
    return pd.DataFrame()

# ── CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { background: #f8fafc !important; }
[data-testid="stHeader"] { display: none; }

/* TOPBAR */
.topbar {
    background: #111827;
    color: #9ca3af;
    padding: 6px 40px;
    font-size: 12px;
    display: flex;
    gap: 24px;
    align-items: center;
}

/* NAVBAR */
.navbar {
    background: white;
    border-bottom: 2px solid #f0fdf4;
    padding: 12px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0 1px 8px rgba(0,0,0,0.06);
}
.nav-brand {
    font-size: 16px;
    font-weight: 800;
    color: #166534;
    display: flex;
    align-items: center;
    gap: 10px;
    letter-spacing: -0.3px;
}
.nav-dot {
    width: 10px; height: 10px;
    background: #22c55e;
    border-radius: 50%;
    animation: blink 2s infinite;
}
@keyframes blink {
    0%,100% { opacity: 1; }
    50% { opacity: 0.3; }
}
.nav-links {
    display: flex;
    gap: 32px;
    font-size: 12px;
    font-weight: 600;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* HERO */
.hero {
    background: linear-gradient(135deg, rgba(0,0,0,0.65) 0%, rgba(0,0,0,0.4) 100%),
                url('https://images.unsplash.com/photo-1597212720158-ae3d645dfdb5?w=1600&q=90') center/cover no-repeat;
    padding: 80px 60px;
    color: white;
    min-height: 320px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.hero-badge {
    display: inline-block;
    background: rgba(34,197,94,0.2);
    border: 1px solid rgba(34,197,94,0.4);
    color: #86efac;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 16px;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1.2;
    max-width: 600px;
    margin-bottom: 12px;
}
.hero-desc {
    font-size: 1rem;
    color: rgba(255,255,255,0.75);
    max-width: 480px;
}

/* ABOUT SECTION */
.about-section {
    padding: 70px 60px;
    background: white;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 70px;
    align-items: center;
}
.about-text h2 { font-size: 1.7rem; font-weight: 800; color: #111; margin-bottom: 16px; }
.about-text p { font-size: 13.5px; color: #555; line-height: 1.85; margin-bottom: 14px; }
.stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 32px; }
.stat-box {
    background: #f0fdf4;
    border-radius: 12px;
    padding: 16px;
    border-left: 3px solid #22c55e;
}
.stat-value { font-size: 1.5rem; font-weight: 800; color: #166534; }
.stat-label { font-size: 11px; color: #6b7280; margin-top: 2px; }
.map-img { width: 100%; border-radius: 16px; box-shadow: 0 8px 30px rgba(0,0,0,0.1); }

/* SECTION */
.section { padding: 60px; background: #f8fafc; }
.section-header { margin-bottom: 40px; }
.section-title { font-size: 1.6rem; font-weight: 800; color: #111; margin-bottom: 6px; }
.section-sub { color: #6b7280; font-size: 0.9rem; }

/* CARDS ACCUEIL */
.space-card {
    background: white;
    border-radius: 20px;
    padding: 36px 28px;
    text-align: center;
    border: 1px solid #e5e7eb;
    transition: all 0.3s;
    height: 100%;
}
.space-card:hover { box-shadow: 0 8px 30px rgba(0,0,0,0.08); transform: translateY(-3px); }
.space-icon { font-size: 2.8rem; margin-bottom: 16px; }
.space-name { font-size: 1.1rem; font-weight: 700; color: #111; margin-bottom: 8px; }
.space-desc { font-size: 13px; color: #6b7280; line-height: 1.6; }

/* INPUTS */
.stTextInput > label { font-weight: 600 !important; color: #374151 !important; font-size: 13px !important; }
.stTextInput > div > div > input {
    border: 1.5px solid #d1fae5 !important;
    border-radius: 10px !important;
    padding: 11px 14px !important;
    font-size: 14px !important;
    background: #f9fafb !important;
    transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #22c55e !important;
    box-shadow: 0 0 0 3px rgba(34,197,94,0.12) !important;
    background: white !important;
}

/* BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, #166534, #15803d) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: all 0.25s !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #14532d, #166534) !important;
    box-shadow: 0 4px 15px rgba(22,101,52,0.3) !important;
    transform: translateY(-1px) !important;
}

/* DASHBOARD */
.dash-header {
    background: linear-gradient(135deg, #166534 0%, #15803d 50%, #16a34a 100%);
    padding: 28px 40px;
    color: white;
    margin-bottom: 0;
}
.dash-title { font-size: 1.3rem; font-weight: 800; margin-bottom: 4px; }
.dash-sub { font-size: 13px; opacity: 0.8; }

/* KPI */
.kpi-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    padding: 24px 40px;
    background: white;
    border-bottom: 1px solid #f0f0f0;
}
.kpi-card {
    background: #f8fafc;
    border-radius: 14px;
    padding: 18px 20px;
    display: flex;
    align-items: center;
    gap: 14px;
    border: 1px solid #e5e7eb;
    transition: all 0.2s;
}
.kpi-card:hover { box-shadow: 0 4px 15px rgba(0,0,0,0.06); transform: translateY(-1px); }
.kpi-icon { font-size: 1.8rem; }
.kpi-info { flex: 1; }
.kpi-value { font-size: 1.8rem; font-weight: 800; color: #111; line-height: 1; }
.kpi-label { font-size: 11px; color: #6b7280; margin-top: 3px; text-transform: uppercase; letter-spacing: 0.5px; }

/* FILTERS */
.filter-bar {
    background: white;
    padding: 16px 40px;
    border-bottom: 1px solid #f0f0f0;
    display: flex;
    gap: 16px;
    align-items: center;
}

/* TABLE */
.stDataFrame { border-radius: 12px !important; overflow: hidden !important; }

/* BADGES */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
}
.badge-pending { background: #fef3c7; color: #92400e; }
.badge-delivered { background: #d1fae5; color: #065f46; }
.badge-erreur { background: #fee2e2; color: #991b1b; }

/* RESULT CARD */
.result-card {
    background: white;
    border-radius: 16px;
    padding: 28px;
    border: 1px solid #e5e7eb;
    margin-top: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.result-title {
    font-size: 1rem;
    font-weight: 700;
    color: #111;
    margin-bottom: 20px;
    padding-bottom: 14px;
    border-bottom: 1.5px solid #f0fdf4;
    display: flex;
    align-items: center;
    gap: 8px;
}
.result-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #f9fafb;
    font-size: 14px;
}
.result-label { color: #6b7280; font-size: 13px; }
.result-value { font-weight: 600; color: #111; }

/* SUPPORT */
.support-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 28px; }
.support-card {
    background: white;
    border-radius: 16px;
    padding: 28px 20px;
    text-align: center;
    border: 1px solid #e5e7eb;
    transition: all 0.2s;
}
.support-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.07); }
.support-icon { font-size: 2rem; margin-bottom: 12px; }
.support-title { font-size: 14px; font-weight: 700; color: #111; margin-bottom: 6px; }
.support-desc { font-size: 12px; color: #6b7280; margin-bottom: 14px; line-height: 1.6; }

/* FOOTER */
.footer { background: #111827; color: white; padding: 50px 60px; }
.footer-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 40px; }
.footer-title { font-size: 11px; font-weight: 700; color: #6b7280; margin-bottom: 14px; text-transform: uppercase; letter-spacing: 1.5px; }
.footer-info { font-size: 13px; line-height: 2.2; color: rgba(255,255,255,0.7); }
.footer-bottom { border-top: 1px solid rgba(255,255,255,0.08); margin-top: 36px; padding-top: 18px; font-size: 12px; color: rgba(255,255,255,0.35); text-align: center; }

/* LOGIN */
.login-hero {
    background: linear-gradient(135deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.45) 100%),
                url('https://images.unsplash.com/photo-1597212720158-ae3d645dfdb5?w=1600&q=90') center/cover no-repeat;
    min-height: 92vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px;
}
.login-card {
    background: white;
    border-radius: 24px;
    padding: 44px 36px;
    width: 100%;
    max-width: 420px;
    box-shadow: 0 30px 80px rgba(0,0,0,0.25);
    border-top: 4px solid #22c55e;
    animation: slideUp 0.4s ease;
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(24px); }
    to { opacity: 1; transform: translateY(0); }
}
.login-logo { text-align: center; font-size: 3rem; margin-bottom: 8px; }
.login-title { text-align: center; color: #166534; font-size: 1.5rem; font-weight: 800; }
.login-sub { text-align: center; color: #9ca3af; font-size: 12px; margin-bottom: 28px; text-transform: uppercase; letter-spacing: 1px; }

.dash-content { padding: 32px 40px; background: #f8fafc; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "home"

# ── NAVBAR ────────────────────────────────────────────────────────
def show_navbar():
    st.markdown("""
    <div class='topbar'>
        <span>📞 080 200 123</span>
        <span>✉️ service.client@srm-ms.ma</span>
        <span style='margin-left:auto;color:#22c55e;font-weight:600;'>● Système en ligne</span>
    </div>
    <div class='navbar'>
        <div class='nav-brand'>
            <div class='nav-dot'></div>
            SRM Marrakech-Safi
        </div>
        <div class='nav-links'>
            <span>Qui sommes-nous</span>
            <span>Publications</span>
            <span>Contact</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────
def show_footer():
    st.markdown("""
    <div class='footer'>
        <div class='footer-grid'>
            <div>
                <div class='footer-title'>SRM Marrakech-Safi</div>
                <div class='footer-info'>📍 Avenue Mohamed VI<br>Marrakech 40000<br>📞 080 200 123<br>✉️ service.client@srm-ms.ma</div>
            </div>
            <div>
                <div class='footer-title'>Nos Services</div>
                <div class='footer-info'>Distribution eau potable<br>Gestion électricité<br>Assainissement liquide<br>Relance client SMS</div>
            </div>
            <div>
                <div class='footer-title'>Liens Utiles</div>
                <div class='footer-info'>Espace client<br>Paiement en ligne<br>Appels d'offres<br>Recrutement</div>
            </div>
        </div>
        <div class='footer-bottom'>© 2025 SRM Marrakech-Safi — Tous droits réservés</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE HOME
# ══════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    show_navbar()

    st.markdown("""
    <div class='hero'>
        <div class='hero-badge'>Société Régionale Multiservices</div>
        <div class='hero-title'>Services de distribution d'eau potable, d'électricité et d'assainissement</div>
        <div class='hero-desc'>La SRM Marrakech-Safi au service de 4.9 millions d'habitants dans la région</div>
    </div>
    <div class='about-section'>
        <div class='about-text'>
            <h2>SRM Marrakech-Safi</h2>
            <p>Entrée en fonctionnement le 1er novembre 2024, la SRM-MS se substitue aux anciens opérateurs de distribution avec un capital de 100 millions de dirhams.</p>
            <p>Créée en vertu de la loi n°83-21, elle couvre l'ensemble de la région Marrakech-Safi (ex-zone ONEE).</p>
            <div class='stats-grid'>
                <div class='stat-box'><div class='stat-value'>780K+</div><div class='stat-label'>Clients eau potable</div></div>
                <div class='stat-box'><div class='stat-value'>1.47M+</div><div class='stat-label'>Clients électricité</div></div>
                <div class='stat-box'><div class='stat-value'>394+</div><div class='stat-label'>Complexes hydrauliques</div></div>
                <div class='stat-box'><div class='stat-value'>4.9M+</div><div class='stat-label'>Population desservie</div></div>
            </div>
        </div>
        <div>
            <img class='map-img' src='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Marrakesh-Safi_region_Morocco.svg/600px-Marrakesh-Safi_region_Morocco.svg.png' />
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("""
    <div class='section-header'>
        <div class='section-title'>Choisissez votre espace</div>
        <div class='section-sub'>Accédez à l'espace qui correspond à votre profil</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns([1, 2.2, 0.6, 2.2, 1])
    with c2:
        st.markdown("""
        <div class='space-card'>
            <div class='space-icon'>🔐</div>
            <div class='space-name'>Espace Administration</div>
            <div class='space-desc'>Tableau de bord SMS, suivi des envois et statistiques en temps réel</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        if st.button("Accéder → Administration", use_container_width=True, key="btn_admin"):
            st.session_state.page = "login_admin"
            st.rerun()

    with c4:
        st.markdown("""
        <div class='space-card'>
            <div class='space-icon'>👤</div>
            <div class='space-name'>Espace Client</div>
            <div class='space-desc'>Consultez vos factures impayées et le statut de vos notifications</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        if st.button("Accéder → Espace Client", use_container_width=True, key="btn_client"):
            st.session_state.page = "client"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    show_footer()

# ══════════════════════════════════════════════════════════════════
# PAGE LOGIN ADMIN
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "login_admin":
    show_navbar()
    st.markdown('<div class="login-hero">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div class='login-card'>
            <div class='login-logo'>💧</div>
            <div class='login-title'>SRM-MS</div>
            <div class='login-sub'>Espace Administration</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        username = st.text_input("👤 Identifiant", placeholder="Votre identifiant")
        password = st.text_input("🔒 Mot de passe", type="password", placeholder="Votre mot de passe")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Se connecter →", use_container_width=True, key="btn_login"):
            if username == "srm" and password == "srm2024":
                st.session_state.logged_in = True
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("❌ Identifiants incorrects")
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("← Retour à l'accueil", use_container_width=True, key="btn_back_login"):
            st.session_state.page = "home"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE DASHBOARD ADMIN
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "dashboard":
    if not st.session_state.logged_in:
        st.session_state.page = "login_admin"
        st.rerun()

    show_navbar()

    # Header
    col_h, col_btn = st.columns([8, 1])
    with col_h:
        st.markdown("""
        <div class='dash-header'>
            <div class='dash-title'>📊 Tableau de bord — Suivi SMS</div>
            <div class='dash-sub'>Société Régionale Multiservices Marrakech-Safi</div>
        </div>
        """, unsafe_allow_html=True)
    with col_btn:
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.button("🚪 Quitter", key="btn_quit"):
            st.session_state.logged_in = False
            st.session_state.page = "home"
            st.rerun()

    # Load data
    df = load_data()

    if df.empty:
        st.info("📭 Aucun SMS envoyé pour le moment.")
        st.stop()

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    total   = len(df)
    pending = len(df[df["statut"] == "PENDING"])
    livre   = len(df[df["statut"] == "DELIVERED"])
    erreur  = len(df[df["statut"] == "ERREUR"])

    # KPIs
    st.markdown(f"""
    <div class='kpi-row'>
        <div class='kpi-card'>
            <div class='kpi-icon'>📨</div>
            <div class='kpi-info'>
                <div class='kpi-value'>{total}</div>
                <div class='kpi-label'>Total envoyés</div>
            </div>
        </div>
        <div class='kpi-card'>
            <div class='kpi-icon'>⏳</div>
            <div class='kpi-info'>
                <div class='kpi-value' style='color:#d97706'>{pending}</div>
                <div class='kpi-label'>En cours</div>
            </div>
        </div>
        <div class='kpi-card'>
            <div class='kpi-icon'>✅</div>
            <div class='kpi-info'>
                <div class='kpi-value' style='color:#059669'>{livre}</div>
                <div class='kpi-label'>Livrés</div>
            </div>
        </div>
        <div class='kpi-card'>
            <div class='kpi-icon'>❌</div>
            <div class='kpi-info'>
                <div class='kpi-value' style='color:#dc2626'>{erreur}</div>
                <div class='kpi-label'>Erreurs</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filters
    st.markdown("<div class='dash-content'>", unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
    with col_f1:
        statuts = ["Tous"] + sorted(df["statut"].unique().tolist())
        choix_statut = st.selectbox("🔍 Statut", statuts)
    with col_f2:
        dates = sorted(df["timestamp"].dt.date.unique(), reverse=True)
        date_choisie = st.selectbox("📅 Date", ["Toutes les dates"] + [str(d) for d in dates])
    with col_f3:
        search = st.text_input("🔎 Recherche", placeholder="Numéro ou contrat...")

    # Apply filters
    df_f = df.copy()
    if choix_statut != "Tous":
        df_f = df_f[df_f["statut"] == choix_statut]
    if date_choisie != "Toutes les dates":
        df_f = df_f[df_f["timestamp"].dt.date == pd.to_datetime(date_choisie).date()]
    if search:
        df_f = df_f[
            df_f["phone"].astype(str).str.contains(search, na=False) |
            df_f["contrat"].astype(str).str.contains(search, na=False)
        ]

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Table avec badges statut
    col_t, col_c = st.columns([2, 1])

    with col_t:
        st.markdown(f"**📋 {len(df_f)} résultat(s)**")
        df_show = df_f.copy()
        df_show["timestamp"] = df_show["timestamp"].dt.strftime("%d/%m/%Y %H:%M")
        df_show = df_show.rename(columns={
            "timestamp": "Date",
            "phone": "Téléphone",
            "contrat": "Contrat",
            "montant": "Montant (DH)",
            "statut": "Statut"
        })
        st.dataframe(
            df_show[["Date","Téléphone","Contrat","Montant (DH)","Statut"]],
            use_container_width=True,
            height=400,
            column_config={
                "Statut": st.column_config.SelectboxColumn(
                    "Statut",
                    options=["PENDING", "DELIVERED", "ERREUR"]
                ),
                "Montant (DH)": st.column_config.NumberColumn(
                    "Montant (DH)",
                    format="%.0f DH"
                )
            }
        )

    with col_c:
        st.markdown("**📊 Répartition**")
        chart_data = df["statut"].value_counts().reset_index()
        chart_data.columns = ["Statut", "Nombre"]
        st.bar_chart(chart_data.set_index("Statut"), color="#16a34a", height=200)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        total_f = len(df_f)
        if total_f > 0:
            st.markdown(f"""
            <div style='background:white;border-radius:12px;padding:16px;border:1px solid #e5e7eb;font-size:13px;'>
                <div style='margin-bottom:8px;font-weight:700;color:#111;'>Résumé filtré</div>
                <div style='display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #f3f4f6;'>
                    <span style='color:#6b7280;'>Total</span><span style='font-weight:600;'>{total_f}</span>
                </div>
                <div style='display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #f3f4f6;'>
                    <span style='color:#d97706;'>En cours</span><span style='font-weight:600;'>{len(df_f[df_f["statut"]=="PENDING"])}</span>
                </div>
                <div style='display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #f3f4f6;'>
                    <span style='color:#059669;'>Livrés</span><span style='font-weight:600;'>{len(df_f[df_f["statut"]=="DELIVERED"])}</span>
                </div>
                <div style='display:flex;justify-content:space-between;padding:6px 0;'>
                    <span style='color:#dc2626;'>Erreurs</span><span style='font-weight:600;'>{len(df_f[df_f["statut"]=="ERREUR"])}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    show_footer()

# ══════════════════════════════════════════════════════════════════
# PAGE CLIENT
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "client":
    show_navbar()

    st.markdown("""
    <div class='hero' style="background: linear-gradient(135deg, rgba(0,0,0,0.65) 0%, rgba(0,0,0,0.4) 100%), url('https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=1600&q=90') center/cover no-repeat;">
        <div class='hero-badge'>Espace Client</div>
        <div class='hero-title'>Consultez vos factures impayées</div>
        <div class='hero-desc'>Entrez votre numéro de téléphone ou numéro de contrat pour consulter votre situation.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("""
    <div class='section-header'>
        <div class='section-title'>🔍 Consulter votre situation</div>
        <div class='section-sub'>Recherchez par numéro de téléphone ou numéro de contrat</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.8, 1])
    with c2:
        recherche = st.text_input("Numéro de téléphone ou contrat", placeholder="Ex: 0612345678 ou N20071207")
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        chercher = st.button("🔍 Rechercher", use_container_width=True, key="btn_search")

        if chercher and recherche.strip():
            supabase = get_supabase()
            r = recherche.strip()
            r_intl = "+212" + r[1:] if r.startswith("0") else r

            if supabase:
                resp = supabase.table("sms_log").select("*").execute()
                df = pd.DataFrame(resp.data) if resp.data else pd.DataFrame()
            else:
                df = pd.DataFrame()

            if not df.empty:
                df["phone"] = df["phone"].astype(str)
                df["contrat"] = df["contrat"].astype(str)
                masque = (
                    df["phone"].str.contains(re.escape(r), case=False, na=False) |
                    df["phone"].str.contains(re.escape(r_intl), case=False, na=False) |
                    df["contrat"].str.contains(re.escape(r), case=False, na=False)
                )
                resultats = df[masque].drop_duplicates(subset=["contrat"])

                if resultats.empty:
                    st.success("✅ Aucune facture impayée trouvée pour ce numéro / contrat.")
                else:
                    for _, row in resultats.iterrows():
                        statut = row["statut"]
                        if statut == "PENDING":
                            badge = "<span class='badge badge-pending'>⏳ En attente de paiement</span>"
                        elif statut == "DELIVERED":
                            badge = "<span class='badge badge-delivered'>✅ Notification envoyée</span>"
                        else:
                            badge = "<span class='badge badge-erreur'>❌ Erreur</span>"

                        st.markdown(f"""
                        <div class='result-card'>
                            <div class='result-title'>📄 Détail de la facture impayée</div>
                            <div class='result-row'>
                                <span class='result-label'>Numéro de contrat</span>
                                <span class='result-value'>{row['contrat']}</span>
                            </div>
                            <div class='result-row'>
                                <span class='result-label'>Montant impayé</span>
                                <span class='result-value' style='color:#dc2626;font-size:1.15rem;font-weight:800;'>{row['montant']} DH</span>
                            </div>
                            <div class='result-row'>
                                <span class='result-label'>Téléphone</span>
                                <span class='result-value'>{row['phone']}</span>
                            </div>
                            <div class='result-row'>
                                <span class='result-label'>Date notification</span>
                                <span class='result-value'>{row['timestamp']}</span>
                            </div>
                            <div class='result-row' style='border:none'>
                                <span class='result-label'>Statut</span>
                                {badge}
                            </div>
                            <div style='margin-top:18px;padding:14px 16px;background:#f0fdf4;border-radius:10px;font-size:13px;color:#166534;border:1px solid #bbf7d0;line-height:1.6;'>
                                💡 Pour régulariser votre situation, veuillez vous rendre à l'agence commerciale la plus proche ou contacter le <strong>080 200 123</strong>.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("Aucune donnée disponible pour le moment.")

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        if st.button("← Retour à l'accueil", use_container_width=True, key="btn_back_client"):
            st.session_state.page = "home"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='padding:60px;background:white;'>
        <div class='section-header' style='text-align:center;'>
            <div class='section-title'>Besoin d'aide ?</div>
            <div class='section-sub'>Notre équipe est disponible pour vous accompagner</div>
        </div>
        <div class='support-grid'>
            <div class='support-card'>
                <div class='support-icon'>📞</div>
                <div class='support-title'>Appel téléphonique</div>
                <div class='support-desc'>Service client du lundi au vendredi de 8h à 17h</div>
                <div style='font-weight:800;color:#166534;font-size:15px;'>080 200 123</div>
            </div>
            <div class='support-card'>
                <div class='support-icon'>✉️</div>
                <div class='support-title'>Email</div>
                <div class='support-desc'>Envoyez votre demande, réponse sous 24h</div>
                <div style='font-weight:700;color:#166534;font-size:13px;'>service.client@srm-ms.ma</div>
            </div>
            <div class='support-card'>
                <div class='support-icon'>📍</div>
                <div class='support-title'>Agence la plus proche</div>
                <div class='support-desc'>Rendez-vous pour régulariser votre situation</div>
                <div style='font-weight:700;color:#166534;font-size:13px;'>Avenue Mohamed VI, Marrakech</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    show_footer()