import streamlit as st
import pandas as pd
import json
import os
import re

LOG_FILE = "data/sms_log.json"

st.set_page_config(page_title="SRM-MS", page_icon="https://www.srm-ms.ma/wp-content/uploads/2024/10/cropped-favicon-srm-32x32.png", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
* { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { background: white !important; }
[data-testid="stHeader"] { display: none; }

.topbar { background: #1a1a1a; color: #ccc; padding: 7px 40px; font-size: 12px; display: flex; gap: 24px; }
.navbar { background: white; border-bottom: 1.5px solid #e5e7eb; padding: 14px 40px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 999; }
.nav-brand { font-size: 15px; font-weight: 700; color: #2e7d32; display: flex; align-items: center; gap: 10px; }
.nav-circle { width: 32px; height: 32px; background: #2e7d32; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 14px; }
.nav-links { display: flex; gap: 28px; font-size: 12px; font-weight: 600; color: #444; }

.hero { background: linear-gradient(rgba(0,0,0,0.52), rgba(0,0,0,0.52)), url('https://images.unsplash.com/photo-1597212720158-ae3d645dfdb5?w=1400&q=80') center/cover no-repeat; padding: 90px 60px; color: white; min-height: 340px; display: flex; flex-direction: column; justify-content: center; }
.hero-sub { font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: #a5d6a7; margin-bottom: 10px; }
.hero-title { font-size: 2.2rem; font-weight: 700; max-width: 620px; line-height: 1.35; }
.hero-desc { font-size: 1rem; color: rgba(255,255,255,0.78); margin-top: 12px; max-width: 480px; }

.about-section { padding: 60px; background: white; display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; }
.about-text h2 { font-size: 1.6rem; font-weight: 700; color: #111; margin-bottom: 16px; }
.about-text p { font-size: 13px; color: #555; line-height: 1.8; margin-bottom: 12px; }
.stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 28px; }
.stat-item .stat-value { font-size: 1.6rem; font-weight: 700; color: #2e7d32; }
.stat-item .stat-label { font-size: 12px; color: #555; margin-top: 2px; line-height: 1.4; }
.map-img { width: 100%; border-radius: 12px; }

.section { padding: 50px 60px; background: #f8fafb; }
.section-title { text-align: center; font-size: 1.5rem; font-weight: 700; color: #111; margin-bottom: 6px; }
.section-sub { text-align: center; color: #6b7280; font-size: 0.9rem; margin-bottom: 32px; }

.stTextInput > label { font-weight: 600 !important; color: #374151 !important; font-size: 13px !important; }
.stTextInput > div > div > input { border: 1.5px solid #d1d5db !important; border-radius: 9px !important; padding: 11px 14px !important; font-size: 14px !important; background: #f9fafb !important; }
.stTextInput > div > div > input:focus { border-color: #2e7d32 !important; box-shadow: 0 0 0 3px rgba(46,125,50,0.12) !important; background: white !important; }

.stButton > button { background: #2e7d32 !important; color: white !important; border: none !important; border-radius: 9px !important; padding: 13px !important; font-size: 14px !important; font-weight: 600 !important; width: 100% !important; transition: all 0.25s !important; }
.stButton > button:hover { background: #1b5e20 !important; }

.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; margin: 28px 0; }
.kpi-card { background: white; border-radius: 13px; padding: 26px 18px; text-align: center; border: 1px solid #e5e7eb; border-top: 4px solid #4caf50; }
.kpi-card.orange { border-top-color: #f59e0b; }
.kpi-card.green2 { border-top-color: #10b981; }
.kpi-card.red { border-top-color: #ef4444; }
.kpi-value { font-size: 2.2rem; font-weight: 700; color: #111; }
.kpi-label { font-size: 13px; color: #6b7280; margin-top: 5px; }

.result-card { background: white; border-radius: 14px; padding: 28px; border: 1px solid #e5e7eb; margin-top: 16px; }
.result-title { font-size: 1rem; font-weight: 700; color: #111; margin-bottom: 16px; border-bottom: 1.5px solid #e5e7eb; padding-bottom: 12px; }
.result-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 0.5px solid #f3f4f6; font-size: 14px; }
.result-label { color: #6b7280; }
.result-value { font-weight: 600; color: #111; }
.badge-pending { background: #fef3c7; color: #92400e; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.badge-delivered { background: #d1fae5; color: #065f46; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.badge-erreur { background: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }

.support-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 28px; }
.support-card { background: white; border-radius: 14px; padding: 28px 20px; text-align: center; border: 1px solid #e5e7eb; }
.support-icon { font-size: 2rem; margin-bottom: 12px; }
.support-title { font-size: 14px; font-weight: 700; color: #111; margin-bottom: 6px; }
.support-desc { font-size: 12px; color: #6b7280; margin-bottom: 14px; line-height: 1.6; }

.footer { background: #1b5e20; color: white; padding: 44px 60px; }
.footer-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 40px; }
.footer-title { font-size: 13px; font-weight: 700; color: #a5d6a7; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px; }
.footer-info { font-size: 13px; line-height: 2.1; color: rgba(255,255,255,0.82); }
.footer-bottom { border-top: 1px solid rgba(255,255,255,0.15); margin-top: 32px; padding-top: 16px; font-size: 12px; color: rgba(255,255,255,0.5); text-align: center; }
.dash-section { padding: 40px 60px; background: #f8fafb; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "home"

# ── NAVBAR ─────────────────────────────────────────────────────────
def show_navbar():
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
            <span>PUBLICATIONS</span>
            <span>CONTACT</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER ─────────────────────────────────────────────────────────
def show_footer():
    st.markdown("""
    <div class='footer'>
        <div class='footer-grid'>
            <div>
                <div class='footer-title'>Infos SRM Marrakech-Safi</div>
                <div class='footer-info'>📍 Avenue Mohamed VI<br>Marrakech 40000<br>📞 0524424300<br>✉️ service.client@srm-ms.ma</div>
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
        <div class='hero-sub'>Société Régionale Multiservices — Marrakech-Safi</div>
        <div class='hero-title'>Services de distribution d'eau potable,<br>d'électricité et de gestion d'assainissement</div>
        <div class='hero-desc'>La SRM Marrakech-Safi au service de 4.9 millions d'habitants</div>
    </div>
    <div class='about-section'>
        <div class='about-text'>
            <h2>SRM Marrakech-Safi</h2>
            <p>Projet ambitieux et étape fondamentale dans l'évolution des services publics, la SRM-MS est entrée en fonctionnement le 1er novembre 2024.</p>
            <p>Créée en vertu de la loi n°83-21, la SRM-MS se substitue aux anciens opérateurs de distribution de la Région avec un capital de 100 millions de dirhams.</p>
            <div class='stats-grid'>
                <div class='stat-item'><div class='stat-value'>780 000 +</div><div class='stat-label'>Clients Eau potable</div></div>
                <div class='stat-item'><div class='stat-value'>1 470 000 +</div><div class='stat-label'>Clients Electricité</div></div>
                <div class='stat-item'><div class='stat-value'>394 +</div><div class='stat-label'>Complexes hydrauliques</div></div>
                <div class='stat-item'><div class='stat-value'>33 +</div><div class='stat-label'>Postes sources Electricité</div></div>
                <div class='stat-item'><div class='stat-value'>15 +</div><div class='stat-label'>Stations d'épuration</div></div>
                <div class='stat-item'><div class='stat-value'>4.9 M +</div><div class='stat-label'>Population desservie</div></div>
            </div>
        </div>
        <div>
            <img class='map-img' src='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Marrakesh-Safi_region_Morocco.svg/600px-Marrakesh-Safi_region_Morocco.svg.png' />
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Choisissez votre espace</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Accédez à l'espace qui correspond à votre profil</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns([1, 2, 0.5, 2, 1])
    with c2:
        st.markdown("""
        <div style='background:white;border-radius:16px;padding:32px;text-align:center;border:1px solid #e5e7eb;'>
            <div style='font-size:2.5rem;margin-bottom:12px;'>🔐</div>
            <div style='font-size:1.1rem;font-weight:700;color:#111;margin-bottom:8px;'>Espace Administration</div>
            <div style='font-size:13px;color:#6b7280;margin-bottom:20px;'>Tableau de bord SMS, suivi des envois et statistiques</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Accéder → Administration", use_container_width=True, key="btn_admin"):
            st.session_state.page = "login_admin"
            st.rerun()

    with c4:
        st.markdown("""
        <div style='background:white;border-radius:16px;padding:32px;text-align:center;border:1px solid #e5e7eb;'>
            <div style='font-size:2.5rem;margin-bottom:12px;'>👤</div>
            <div style='font-size:1.1rem;font-weight:700;color:#111;margin-bottom:8px;'>Espace Client</div>
            <div style='font-size:13px;color:#6b7280;margin-bottom:20px;'>Consultez vos factures impayées et le statut de vos contrats</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
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
    st.markdown("""
    <div class='hero'>
        <div class='hero-sub'>Administration — SRM Marrakech-Safi</div>
        <div class='hero-title'>Espace Administration</div>
        <div class='hero-desc'>Connectez-vous pour accéder au tableau de bord SMS</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🔐 Connexion Administration</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Entrez vos identifiants pour accéder au tableau de bord</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        username = st.text_input("Nom d'utilisateur", placeholder="Identifiant")
        password = st.text_input("Mot de passe", type="password", placeholder="Mot de passe")
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("Se connecter →", use_container_width=True, key="btn_login"):
            if username == "srm" and password == "srm2024":
                st.session_state.logged_in = True
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Identifiants incorrects.")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("← Retour à l'accueil", use_container_width=True, key="btn_back_login"):
            st.session_state.page = "home"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    show_footer()

# ══════════════════════════════════════════════════════════════════
# PAGE DASHBOARD ADMIN
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "dashboard":
    if not st.session_state.logged_in:
        st.session_state.page = "login_admin"
        st.rerun()

    show_navbar()

    c_sp, c_btn = st.columns([9, 1])
    with c_btn:
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("🚪 Quitter", key="btn_quit"):
            st.session_state.logged_in = False
            st.session_state.page = "home"
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
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    total   = len(df)
    pending = len(df[df["statut"] == "PENDING"])
    livre   = len(df[df["statut"] == "DELIVERED"])
    erreur  = len(df[df["statut"] == "ERREUR"])

    st.markdown(f"""
    <div class='kpi-grid'>
        <div class='kpi-card'><div class='kpi-value'>{total}</div><div class='kpi-label'>📨 Total SMS</div></div>
        <div class='kpi-card orange'><div class='kpi-value' style='color:#f59e0b'>{pending}</div><div class='kpi-label'>⏳ En cours</div></div>
        <div class='kpi-card green2'><div class='kpi-value' style='color:#10b981'>{livre}</div><div class='kpi-label'>✅ Livrés</div></div>
        <div class='kpi-card red'><div class='kpi-value' style='color:#ef4444'>{erreur}</div><div class='kpi-label'>❌ Erreurs</div></div>
    </div>
    """, unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        statuts = ["Tous"] + sorted(df["statut"].unique().tolist())
        choix_statut = st.selectbox("🔍 Filtrer par statut", statuts)
    with col_f2:
        date_min = df["timestamp"].min().date()
        date_max = df["timestamp"].max().date()
        date_debut = st.date_input("📅 Date début", value=date_min, min_value=date_min, max_value=date_max)
    with col_f3:
        date_fin = st.date_input("📅 Date fin", value=date_max, min_value=date_min, max_value=date_max)

    df_filtré = df.copy()
    if choix_statut != "Tous":
        df_filtré = df_filtré[df_filtré["statut"] == choix_statut]
    df_filtré = df_filtré[
        (df_filtré["timestamp"].dt.date >= date_debut) &
        (df_filtré["timestamp"].dt.date <= date_fin)
    ]

    df_affiche = df_filtré.copy()
    df_affiche["timestamp"] = df_affiche["timestamp"].dt.strftime("%Y-%m-%d %H:%M")

    st.markdown(f"<div style='font-size:13px;color:#6b7280;margin-bottom:8px;'>{len(df_affiche)} résultat(s) trouvé(s)</div>", unsafe_allow_html=True)
    st.dataframe(df_affiche[["timestamp","phone","contrat","montant","statut"]], use_container_width=True, height=360)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.subheader("📊 Répartition des statuts")
    st.bar_chart(df["statut"].value_counts())
    st.markdown("</div>", unsafe_allow_html=True)
    show_footer()

# ══════════════════════════════════════════════════════════════════
# PAGE CLIENT
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "client":
    show_navbar()
    st.markdown("""
    <div class='hero' style="background: linear-gradient(rgba(0,0,0,0.52), rgba(0,0,0,0.52)), url('https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=1400&q=80') center/cover no-repeat;">
        <div class='hero-sub'>Espace Client — SRM Marrakech-Safi</div>
        <div class='hero-title'>Consultez vos factures impayées</div>
        <div class='hero-desc'>Entrez votre numéro de téléphone ou numéro de contrat pour consulter votre situation.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🔍 Consulter votre situation</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Recherchez par numéro de téléphone ou numéro de contrat</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        recherche = st.text_input("Numéro de téléphone ou contrat", placeholder="Ex: 0612345678 ou N20071207")
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        chercher = st.button("Rechercher →", use_container_width=True, key="btn_search")

        if chercher and recherche.strip():
            if not os.path.exists(LOG_FILE):
                st.warning("Aucune donnée disponible pour le moment.")
            else:
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    log = json.load(f)
                df = pd.DataFrame(log)

                r = recherche.strip()
                r_intl = "+212" + r[1:] if r.startswith("0") else r

                df["phone"] = df["phone"].astype(str)
                df["contrat"] = df["contrat"].astype(str)

                masque = (
                    df["phone"].str.contains(re.escape(r), case=False, na=False) |
                    df["phone"].str.contains(re.escape(r_intl), case=False, na=False) |
                    df["contrat"].str.contains(re.escape(r), case=False, na=False)
                )
                resultats = df[masque].drop_duplicates(subset=["contrat"])

                if resultats.empty:
                    st.info("✅ Aucune facture impayée trouvée pour ce numéro / contrat.")
                else:
                    for _, row in resultats.iterrows():
                        statut = row["statut"]
                        if statut == "PENDING":
                            badge = "<span class='badge-pending'>⏳ En attente de paiement</span>"
                        elif statut == "DELIVERED":
                            badge = "<span class='badge-delivered'>✅ Notification envoyée</span>"
                        else:
                            badge = "<span class='badge-erreur'>❌ Erreur notification</span>"

                        st.markdown(f"""
                        <div class='result-card'>
                            <div class='result-title'>📄 Détail de la facture impayée</div>
                            <div class='result-row'>
                                <span class='result-label'>Numéro de contrat</span>
                                <span class='result-value'>{row['contrat']}</span>
                            </div>
                            <div class='result-row'>
                                <span class='result-label'>Montant impayé</span>
                                <span class='result-value' style='color:#ef4444;font-size:1.1rem'>{row['montant']} DH</span>
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
                            <div style='margin-top:16px;padding:14px;background:#f0fdf4;border-radius:10px;font-size:13px;color:#166534;border:1px solid #bbf7d0;'>
                                💡 Pour régulariser votre situation, veuillez vous rendre à l'agence commerciale la plus proche ou contacter le <strong>080200123</strong>.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        if st.button("← Retour à l'accueil", use_container_width=True, key="btn_back_client"):
            st.session_state.page = "home"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='padding:50px 60px;background:white;'>
        <div class='section-title'>Besoin d'aide ?</div>
        <div class='section-sub'>Notre équipe est disponible pour vous accompagner</div>
        <div class='support-grid'>
            <div class='support-card'>
                <div class='support-icon'>📞</div>
                <div class='support-title'>Appel téléphonique</div>
                <div class='support-desc'>Service client du lundi au vendredi de 8h à 17h</div>
                <div style='font-weight:700;color:#2e7d32;font-size:15px;'>080200123</div>
            </div>
            <div class='support-card'>
                <div class='support-icon'>✉️</div>
                <div class='support-title'>Email</div>
                <div class='support-desc'>Envoyez votre demande, réponse sous 24h</div>
                <div style='font-weight:700;color:#2e7d32;font-size:13px;'>service.client@srm-ms.ma</div>
            </div>
            <div class='support-card'>
                <div class='support-icon'>📍</div>
                <div class='support-title'>Agence la plus proche</div>
                <div class='support-desc'>Rendez-vous pour régulariser votre situation</div>
                <div style='font-weight:700;color:#2e7d32;font-size:13px;'>Avenue Mohamed VI, Marrakech</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    show_footer()