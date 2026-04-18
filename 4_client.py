import streamlit as st
import pandas as pd
import json
import os

LOG_FILE = "data/sms_log.json"

st.set_page_config(page_title="SRM-MS - Espace Client", page_icon="💧", layout="wide", initial_sidebar_state="collapsed")

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
.nav-brand { font-size: 15px; font-weight: 700; color: #2e7d32; }
.nav-links { display: flex; gap: 28px; font-size: 12px; font-weight: 600; color: #444; }

.hero {
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
    url('https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=1400&q=80') center/cover no-repeat;
    padding: 80px 60px; color: white; min-height: 300px;
    display: flex; flex-direction: column; justify-content: center;
}
.hero-sub { font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: #a5d6a7; margin-bottom: 10px; }
.hero-title { font-size: 2rem; font-weight: 700; max-width: 600px; line-height: 1.35; }
.hero-desc { font-size: 0.95rem; color: rgba(255,255,255,0.78); margin-top: 10px; max-width: 460px; }

.section { padding: 50px 60px; background: #f8fafb; }
.section-title { text-align: center; font-size: 1.5rem; font-weight: 700; color: #111; margin-bottom: 6px; }
.section-sub { text-align: center; color: #6b7280; font-size: 0.9rem; margin-bottom: 32px; }

.stTextInput > label { font-weight: 600 !important; color: #374151 !important; font-size: 13px !important; }
.stTextInput > div > div > input { border: 1.5px solid #d1d5db !important; border-radius: 9px !important; padding: 11px 14px !important; font-size: 14px !important; background: #f9fafb !important; }
.stTextInput > div > div > input:focus { border-color: #2e7d32 !important; box-shadow: 0 0 0 3px rgba(46,125,50,0.12) !important; background: white !important; }

.stButton > button { background: #2e7d32 !important; color: white !important; border: none !important; border-radius: 9px !important; padding: 13px !important; font-size: 14px !important; font-weight: 600 !important; width: 100% !important; }
.stButton > button:hover { background: #1b5e20 !important; }

.result-card { background: white; border-radius: 14px; padding: 28px; border: 1px solid #e5e7eb; margin-top: 20px; }
.result-title { font-size: 1rem; font-weight: 700; color: #111; margin-bottom: 16px; border-bottom: 1.5px solid #e5e7eb; padding-bottom: 12px; }
.result-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 0.5px solid #f3f4f6; font-size: 14px; }
.result-label { color: #6b7280; }
.result-value { font-weight: 600; color: #111; }
.badge-pending { background: #fef3c7; color: #92400e; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.badge-delivered { background: #d1fae5; color: #065f46; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.badge-erreur { background: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }

.support-section { background: white; padding: 50px 60px; }
.support-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 28px; }
.support-card { background: #f8fafb; border-radius: 14px; padding: 28px 20px; text-align: center; border: 1px solid #e5e7eb; }
.support-icon { font-size: 2rem; margin-bottom: 12px; }
.support-title { font-size: 14px; font-weight: 700; color: #111; margin-bottom: 6px; }
.support-desc { font-size: 12px; color: #6b7280; margin-bottom: 14px; line-height: 1.6; }
.support-btn { background: #2e7d32; color: white; border: none; border-radius: 8px; padding: 9px 20px; font-size: 12px; font-weight: 600; cursor: pointer; }

.footer { background: #1b5e20; color: white; padding: 44px 60px; }
.footer-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 40px; }
.footer-title { font-size: 13px; font-weight: 700; color: #a5d6a7; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px; }
.footer-info { font-size: 13px; line-height: 2.1; color: rgba(255,255,255,0.82); }
.footer-bottom { border-top: 1px solid rgba(255,255,255,0.15); margin-top: 32px; padding-top: 16px; font-size: 12px; color: rgba(255,255,255,0.5); text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='topbar'>
    <span>📞 Tél : 080200123</span>
    <span>✉️ service.client@srm-ms.ma</span>
</div>
<div class='navbar'>
    <div class='nav-brand'>💧 SRM Marrakech-Safi</div>
    <div class='nav-links'>
        <span>QUI SOMMES-NOUS</span>
        <span>ESPACE CLIENT</span>
        <span>PUBLICATIONS</span>
        <span>CONTACT</span>
    </div>
</div>
<div class='hero'>
    <div class='hero-sub'>Société Régionale Multiservices — Marrakech-Safi</div>
    <div class='hero-title'>Espace Client</div>
    <div class='hero-desc'>Consultez vos factures impayées et le statut de vos contrats en toute simplicité.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🔍 Consulter votre situation</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Entrez votre numéro de téléphone ou numéro de contrat</div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 1.5, 1])
with c2:
    recherche = st.text_input("Numéro de téléphone ou numéro de contrat", placeholder="Ex: 0612345678 ou CTR-001")
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    chercher = st.button("Rechercher →", use_container_width=True)

if chercher and recherche:
    if not os.path.exists(LOG_FILE):
        st.warning("Aucune donnée disponible pour le moment.")
    else:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            log = json.load(f)
        df = pd.DataFrame(log)

        recherche_clean = recherche.strip()
        if recherche_clean.startswith("0"):
            recherche_intl = "+212" + recherche_clean[1:]
        else:
            recherche_intl = recherche_clean

        masque = (
            df["phone"].str.contains(recherche_clean, case=False, na=False) |
            df["phone"].str.contains(recherche_intl, case=False, na=False) |
            df["contrat"].str.contains(recherche_clean, case=False, na=False)
        )
        resultats = df[masque]

        with c2:
            if resultats.empty:
                st.info("Aucune facture impayée trouvée pour ce numéro / contrat.")
            else:
                for _, row in resultats.iterrows():
                    statut = row["statut"]
                    if statut == "PENDING":
                        badge = "<span class='badge-pending'>⏳ En attente</span>"
                    elif statut == "DELIVERED":
                        badge = "<span class='badge-delivered'>✅ Notifié</span>"
                    else:
                        badge = "<span class='badge-erreur'>❌ Erreur</span>"

                    st.markdown(f"""
                    <div class='result-card'>
                        <div class='result-title'>📄 Détail de la facture</div>
                        <div class='result-row'>
                            <span class='result-label'>Numéro de contrat</span>
                            <span class='result-value'>{row['contrat']}</span>
                        </div>
                        <div class='result-row'>
                            <span class='result-label'>Montant impayé</span>
                            <span class='result-value' style='color:#ef4444; font-size:1.1rem'>{row['montant']} DH</span>
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
                        <div style='margin-top:16px; padding:14px; background:#f0fdf4; border-radius:10px; font-size:13px; color:#166534; border:1px solid #bbf7d0;'>
                            💡 Pour régulariser votre situation, veuillez vous rendre à l'agence commerciale la plus proche ou contacter le <strong>080200123</strong>.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class='support-section'>
    <div class='section-title'>Besoin d'aide ?</div>
    <div class='section-sub'>Notre équipe est disponible pour vous accompagner</div>
    <div class='support-grid'>
        <div class='support-card'>
            <div class='support-icon'>📞</div>
            <div class='support-title'>Appel téléphonique</div>
            <div class='support-desc'>Contactez notre service client du lundi au vendredi de 8h à 17h</div>
            <div style='font-weight:700; color:#2e7d32; font-size:15px;'>080200123</div>
        </div>
        <div class='support-card'>
            <div class='support-icon'>✉️</div>
            <div class='support-title'>Email</div>
            <div class='support-desc'>Envoyez-nous votre demande par email, réponse sous 24h</div>
            <div style='font-weight:700; color:#2e7d32; font-size:13px;'>service.client@srm-ms.ma</div>
        </div>
        <div class='support-card'>
            <div class='support-icon'>📍</div>
            <div class='support-title'>Agence la plus proche</div>
            <div class='support-desc'>Rendez-vous dans l'une de nos agences pour régulariser votre situation</div>
            <div style='font-weight:700; color:#2e7d32; font-size:13px;'>Avenue Mohamed VI, Marrakech</div>
        </div>
    </div>
</div>

<div class='footer'>
    <div class='footer-grid'>
        <div>
            <div class='footer-title'>Infos SRM Marrakech-Safi</div>
            <div class='footer-info'>
                📍 Avenue Mohamed VI<br>
                Marrakech 40000<br>
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