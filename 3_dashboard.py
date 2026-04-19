import streamlit as st
import base64
import os
import pandas as pd
import re
from datetime import date

st.set_page_config(
    page_title="SRM-MS — Système SMS",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── IMAGES ───────────────────────────────────────────────────────
def get_img_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

img1 = get_img_b64("assets/marrakech.jpg")
img2 = get_img_b64("assets/marrakech2.jpg")
bg1 = f"url('data:image/jpeg;base64,{img1}')" if img1 else "url('https://images.unsplash.com/photo-1597212720158-ae3d645dfdb5?w=1600&q=90')"
bg2 = f"url('data:image/jpeg;base64,{img2}')" if img2 else "url('https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=1600&q=90')"

# ── CSS ───────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* {{ font-family: 'Inter', sans-serif !important; box-sizing: border-box; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 0 !important; max-width: 100% !important; }}
[data-testid="stAppViewContainer"] {{ background: #f8fafc !important; }}
[data-testid="stHeader"] {{ display: none; }}

/* Hide nav buttons */
[data-testid="stButton"] {{ display: none !important; }}
[data-testid="stButton"].nav-btn {{ display: block !important; }}

.topbar {{
    background: #111827; color: #9ca3af;
    padding: 6px 40px; font-size: 12px;
    display: flex; align-items: center; gap: 24px;
}}
.topbar-right {{
    margin-left: auto; color: #22c55e;
    font-weight: 600; display: flex; align-items: center; gap: 6px;
}}
.navbar {{
    background: white; border-bottom: 2px solid #f0fdf4;
    padding: 0 40px; display: flex; align-items: center;
    justify-content: space-between; position: sticky;
    top: 0; z-index: 999; box-shadow: 0 1px 8px rgba(0,0,0,0.06); height: 60px;
}}
.nav-brand {{
    font-size: 16px; font-weight: 800; color: #166534;
    display: flex; align-items: center; gap: 8px;
}}
.nav-dot {{
    width: 9px; height: 9px; background: #22c55e;
    border-radius: 50%; animation: blink 2s infinite;
}}
@keyframes blink {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:0.3; }} }}
.nav-links {{ display: flex; gap: 4px; align-items: center; }}
.nav-link {{
    padding: 8px 16px; border-radius: 8px; font-size: 13px;
    font-weight: 600; color: #6b7280; cursor: pointer;
    transition: all 0.2s; text-transform: uppercase; letter-spacing: 0.5px;
}}
.nav-link:hover {{ background: #f0fdf4; color: #166534; }}
.nav-link.active {{ background: #f0fdf4; color: #166534; }}

.hero {{
    background: linear-gradient(135deg, rgba(0,0,0,0.65) 0%, rgba(0,0,0,0.4) 100%), {bg1} center/cover no-repeat;
    padding: 80px 60px; color: white; min-height: 340px;
    display: flex; flex-direction: column; justify-content: center;
    background-size: cover !important; background-position: center !important;
}}
.hero-badge {{
    display: inline-block; background: rgba(34,197,94,0.2);
    border: 1px solid rgba(34,197,94,0.4); color: #86efac;
    padding: 4px 14px; border-radius: 20px; font-size: 11px;
    font-weight: 600; letter-spacing: 2px; text-transform: uppercase;
    margin-bottom: 16px; width: fit-content;
}}
.hero-title {{ font-size: 2.2rem; font-weight: 800; line-height: 1.25; max-width: 600px; margin-bottom: 10px; }}
.hero-desc {{ font-size: 1rem; color: rgba(255,255,255,0.75); max-width: 480px; }}

.section {{ padding: 48px 60px; }}
.section-bg {{ background: white; }}
.section-title {{ font-size: 1.4rem; font-weight: 800; color: #111; margin-bottom: 4px; }}
.section-sub {{ color: #6b7280; font-size: 0.9rem; margin-bottom: 28px; }}

.card {{
    background: white; border-radius: 16px; padding: 28px;
    border: 1px solid #e5e7eb; box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}}

.kpi-row {{
    display: grid; grid-template-columns: repeat(4,1fr);
    gap: 16px; padding: 20px 60px;
    background: white; border-bottom: 1px solid #f3f4f6;
}}
.kpi-card {{
    background: #f8fafc; border-radius: 14px; padding: 20px;
    display: flex; align-items: center; gap: 14px; border: 1px solid #e5e7eb;
}}
.kpi-icon {{ font-size: 1.8rem; }}
.kpi-value {{ font-size: 1.8rem; font-weight: 800; color: #111; line-height: 1; }}
.kpi-label {{ font-size: 11px; color: #6b7280; margin-top: 3px; text-transform: uppercase; letter-spacing: 0.5px; }}

.stTextInput > label {{ font-weight: 600 !important; color: #374151 !important; font-size: 13px !important; }}
.stTextInput > div > div > input {{
    border: 1.5px solid #d1fae5 !important; border-radius: 10px !important;
    padding: 11px 14px !important; font-size: 14px !important;
    background: #f9fafb !important; color: #111 !important;
}}
.stTextInput > div > div > input:focus {{
    border-color: #22c55e !important;
    box-shadow: 0 0 0 3px rgba(34,197,94,0.12) !important;
    background: white !important;
}}
.stTextArea > label {{ font-weight: 600 !important; color: #374151 !important; font-size: 13px !important; }}
.stTextArea > div > div > textarea {{
    border: 1.5px solid #d1fae5 !important; border-radius: 10px !important;
    font-size: 14px !important; background: #f9fafb !important; color: #111 !important;
}}
.stButton > button {{
    background: linear-gradient(135deg, #166534, #15803d) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; padding: 12px !important;
    font-size: 14px !important; font-weight: 600 !important;
    transition: all 0.25s !important;
}}
.stButton > button:hover {{
    background: linear-gradient(135deg, #14532d, #166534) !important;
    box-shadow: 0 4px 15px rgba(22,101,52,0.3) !important;
    transform: translateY(-1px) !important;
}}

/* Nav buttons hidden */
.nav-hidden button {{
    visibility: hidden !important;
    height: 0px !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
    position: absolute !important;
}}

.badge {{ display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }}
.badge-pending {{ background: #fef3c7; color: #92400e; }}
.badge-delivered {{ background: #d1fae5; color: #065f46; }}
.badge-erreur {{ background: #fee2e2; color: #991b1b; }}

.pub-card {{
    background: white; border-radius: 14px; padding: 24px;
    border: 1px solid #e5e7eb; border-top: 3px solid #22c55e;
}}
.pub-icon {{ font-size: 2rem; margin-bottom: 12px; }}
.pub-title {{ font-size: 15px; font-weight: 700; color: #111; margin-bottom: 8px; }}
.pub-desc {{ font-size: 13px; color: #6b7280; line-height: 1.7; }}

.footer {{ background: #111827; color: white; padding: 44px 60px; }}
.footer-grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 40px; }}
.footer-title {{ font-size: 11px; font-weight: 700; color: #6b7280; margin-bottom: 14px; text-transform: uppercase; letter-spacing: 1.5px; }}
.footer-info {{ font-size: 13px; line-height: 2.2; color: rgba(255,255,255,0.7); }}
.footer-bottom {{ border-top: 1px solid rgba(255,255,255,0.08); margin-top: 36px; padding-top: 18px; font-size: 12px; color: rgba(255,255,255,0.35); text-align: center; }}

.login-hero {{
    min-height: 100vh;
    background: linear-gradient(135deg, rgba(0,0,0,0.72) 0%, rgba(0,0,0,0.48) 100%), {bg1} center/cover no-repeat;
    background-size: cover !important;
    display: flex; align-items: center; justify-content: center; padding: 40px;
}}
.login-card {{
    background: white; border-radius: 24px; padding: 44px 36px;
    width: 100%; max-width: 400px; border-top: 4px solid #22c55e;
    box-shadow: 0 30px 80px rgba(0,0,0,0.25);
}}
.login-logo {{ text-align: center; margin-bottom: 12px; }}
.login-logo img {{ width: 80px; height: 80px; border-radius: 50%; object-fit: cover; }}
.login-title {{ text-align: center; color: #166534; font-size: 1.4rem; font-weight: 800; }}
.login-sub {{ text-align: center; color: #9ca3af; font-size: 12px; margin-bottom: 28px; text-transform: uppercase; letter-spacing: 1px; }}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "home"

# ── TOPBAR ────────────────────────────────────────────────────────
def show_topbar():
    st.markdown("""
    <div class='topbar'>
        <span>📞 080 200 123</span>
        <span>✉️ service.client@srm-ms.ma</span>
        <div class='topbar-right'>
            <div style='width:7px;height:7px;background:#22c55e;border-radius:50%;'></div>
            Système en ligne
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── NAVBAR ────────────────────────────────────────────────────────
def show_navbar(active="home"):
    pages = [
        ("home", "Accueil"),
        ("qui_sommes", "Qui sommes-nous"),
        ("publications", "Publications"),
        ("contact", "Contact"),
    ]
    links_html = "".join([
        f"<div class='nav-link {'active' if active == key else ''}'>{label}</div>"
        for key, label in pages
    ])
    st.markdown(f"""
    <div class='navbar'>
        <div class='nav-brand'>
            <div class='nav-dot'></div>
            SRM Marrakech-Safi
        </div>
        <div class='nav-links'>{links_html}</div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation buttons — cachés visuellement
    st.markdown("<div class='nav-hidden'>", unsafe_allow_html=True)
    cols = st.columns(len(pages) + 4)
    for i, (key, label) in enumerate(pages):
        with cols[i]:
            if st.button(label, key=f"nav_{key}"):
                st.session_state.page = key
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

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
    show_topbar()
    show_navbar("home")
    st.markdown("""
    <div class='hero'>
        <div class='hero-badge'>Société Régionale Multiservices — Marrakech-Safi</div>
        <div class='hero-title'>Système Automatisé de<br>Relance Client par SMS</div>
        <div class='hero-desc'>Gérez vos relances, consultez vos factures et suivez les envois en temps réel.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Choisissez votre espace</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Accédez à l'espace adapté à votre profil</div>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns([1, 2, 0.5, 2, 1])
    with c2:
        st.markdown("""
        <div class='card' style='text-align:center;'>
            <div style='font-size:2.5rem;margin-bottom:12px;'>🔐</div>
            <div style='font-size:1.1rem;font-weight:700;color:#111;margin-bottom:8px;'>Administration</div>
            <div style='font-size:13px;color:#6b7280;line-height:1.6;'>Dashboard SMS, envoi manuel, historique et paramètres</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Accéder → Administration", use_container_width=True, key="go_admin"):
            st.session_state.page = "login_admin"
            st.rerun()
    with c4:
        st.markdown("""
        <div class='card' style='text-align:center;'>
            <div style='font-size:2.5rem;margin-bottom:12px;'>👤</div>
            <div style='font-size:1.1rem;font-weight:700;color:#111;margin-bottom:8px;'>Espace Client</div>
            <div style='font-size:13px;color:#6b7280;line-height:1.6;'>Consultez vos factures impayées et le statut de vos contrats</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("Accéder → Espace Client", use_container_width=True, key="go_client"):
            st.session_state.page = "client"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='padding:48px 60px;background:white;display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center;'>
        <div>
            <div style='font-size:1.4rem;font-weight:800;color:#111;margin-bottom:14px;'>SRM Marrakech-Safi</div>
            <p style='font-size:13.5px;color:#555;line-height:1.85;margin-bottom:12px;'>Entrée en fonctionnement le 1er novembre 2024, la SRM-MS se substitue aux anciens opérateurs avec un capital de 100 millions de dirhams.</p>
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:20px;'>
                <div style='background:#f0fdf4;border-radius:12px;padding:16px;border-left:3px solid #22c55e;'><div style='font-size:1.4rem;font-weight:800;color:#166534;'>780K+</div><div style='font-size:11px;color:#6b7280;margin-top:2px;'>Clients eau potable</div></div>
                <div style='background:#f0fdf4;border-radius:12px;padding:16px;border-left:3px solid #22c55e;'><div style='font-size:1.4rem;font-weight:800;color:#166534;'>1.47M+</div><div style='font-size:11px;color:#6b7280;margin-top:2px;'>Clients électricité</div></div>
                <div style='background:#f0fdf4;border-radius:12px;padding:16px;border-left:3px solid #22c55e;'><div style='font-size:1.4rem;font-weight:800;color:#166534;'>394+</div><div style='font-size:11px;color:#6b7280;margin-top:2px;'>Complexes hydrauliques</div></div>
                <div style='background:#f0fdf4;border-radius:12px;padding:16px;border-left:3px solid #22c55e;'><div style='font-size:1.4rem;font-weight:800;color:#166534;'>4.9M+</div><div style='font-size:11px;color:#6b7280;margin-top:2px;'>Population desservie</div></div>
            </div>
        </div>
        <div>
            <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Marrakesh-Safi_region_Morocco.svg/600px-Marrakesh-Safi_region_Morocco.svg.png' style='width:100%;border-radius:16px;'/>
        </div>
    </div>
    """, unsafe_allow_html=True)
    show_footer()

# ══════════════════════════════════════════════════════════════════
# PAGE LOGIN
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "login_admin":
    show_topbar()
    show_navbar()
    st.markdown('<div class="login-hero">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        # Logo SRM
        logo_b64 = get_img_b64("assets/logo.png")
        if logo_b64:
            logo_html = f"<img src='data:image/png;base64,{logo_b64}' style='width:80px;height:80px;border-radius:50%;object-fit:cover;display:block;margin:0 auto 12px auto;'/>"
        else:
            logo_html = "<div style='font-size:3rem;text-align:center;margin-bottom:12px;'>💧</div>"

        st.markdown(f"""
        <div class='login-card'>
            <div class='login-logo'>{logo_html}</div>
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
        if st.button("← Retour", use_container_width=True, key="btn_back"):
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

    from utils.db import load_sms_log, load_settings, save_settings
    from utils.sms import send_single_sms
    from utils.db import log_sms

    show_topbar()
    st.markdown("""
    <div class='navbar'>
        <div class='nav-brand'>
            <div class='nav-dot'></div>
            SRM — Administration
        </div>
    </div>
    """, unsafe_allow_html=True)

    c_tabs, c_quit = st.columns([9, 1])
    with c_tabs:
        tabs = st.tabs(["📊 Dashboard", "📤 Envoi SMS", "📋 Historique", "⚙️ Paramètres"])
    with c_quit:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("🚪 Quitter", key="quit"):
            st.session_state.logged_in = False
            st.session_state.page = "home"
            st.rerun()

    df = load_sms_log()

    # ── TAB 1: DASHBOARD ──────────────────────────────────────────
    with tabs[0]:
        if df.empty:
            st.info("📭 Aucun SMS envoyé pour le moment.")
        else:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            total   = len(df)
            pending = len(df[df["statut"] == "PENDING"])
            livre   = len(df[df["statut"] == "DELIVERED"])
            erreur  = len(df[df["statut"] == "ERREUR"])

            st.markdown(f"""
            <div class='kpi-row'>
                <div class='kpi-card'><div class='kpi-icon'>📨</div><div><div class='kpi-value'>{total}</div><div class='kpi-label'>Total envoyés</div></div></div>
                <div class='kpi-card'><div class='kpi-icon'>⏳</div><div><div class='kpi-value' style='color:#d97706'>{pending}</div><div class='kpi-label'>En cours</div></div></div>
                <div class='kpi-card'><div class='kpi-icon'>✅</div><div><div class='kpi-value' style='color:#059669'>{livre}</div><div class='kpi-label'>Livrés</div></div></div>
                <div class='kpi-card'><div class='kpi-icon'>❌</div><div><div class='kpi-value' style='color:#dc2626'>{erreur}</div><div class='kpi-label'>Erreurs</div></div></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div class='section'>", unsafe_allow_html=True)

            # Filtre date par défaut = lyouma
            today = date.today()
            dates_dispos = sorted(df["timestamp"].dt.date.unique(), reverse=True)
            dates_options = [str(d) for d in dates_dispos]
            default_idx = dates_options.index(str(today)) if str(today) in dates_options else 0

            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                statuts = ["Tous"] + sorted(df["statut"].unique().tolist())
                choix_statut = st.selectbox("🔍 Statut", statuts)
            with col2:
                date_choisie = st.selectbox(
                    "📅 Date",
                    ["Toutes"] + dates_options,
                    index=default_idx + 1 if str(today) in dates_options else 0
                )
            with col3:
                search = st.text_input("🔎 Recherche", placeholder="Numéro ou contrat...")

            df_f = df.copy()
            if choix_statut != "Tous":
                df_f = df_f[df_f["statut"] == choix_statut]
            if date_choisie != "Toutes":
                df_f = df_f[df_f["timestamp"].dt.date == pd.to_datetime(date_choisie).date()]
            if search:
                df_f = df_f[
                    df_f["phone"].astype(str).str.contains(re.escape(search), na=False) |
                    df_f["contrat"].astype(str).str.contains(re.escape(search), na=False)
                ]

            col_t, col_c = st.columns([2, 1])
            with col_t:
                st.markdown(f"**📋 {len(df_f)} résultat(s)**")
                df_show = df_f.copy()
                df_show["timestamp"] = df_show["timestamp"].dt.strftime("%d/%m/%Y %H:%M")
                df_show = df_show.rename(columns={"timestamp":"Date","phone":"Téléphone","contrat":"Contrat","montant":"Montant","statut":"Statut"})
                st.dataframe(df_show[["Date","Téléphone","Contrat","Montant","Statut"]], use_container_width=True, height=400)

            with col_c:
                st.markdown("**📊 Répartition**")
                import math
                chart_data = df["statut"].value_counts().reset_index()
                chart_data.columns = ["Statut", "Nombre"]
                color_map = {"PENDING": "#f59e0b", "DELIVERED": "#22c55e", "ERREUR": "#ef4444"}
                total_chart = chart_data["Nombre"].sum()
                start = -90
                paths = ""
                for _, row in chart_data.iterrows():
                    pct = row["Nombre"] / total_chart
                    angle = pct * 360
                    color = color_map.get(row["Statut"], "#6b7280")
                    x1 = 100 + 85 * math.cos(math.radians(start))
                    y1 = 100 + 85 * math.sin(math.radians(start))
                    x2 = 100 + 85 * math.cos(math.radians(start + angle))
                    y2 = 100 + 85 * math.sin(math.radians(start + angle))
                    large = 1 if angle > 180 else 0
                    paths += f'<path d="M100,100 L{x1:.1f},{y1:.1f} A85,85 0 {large},1 {x2:.1f},{y2:.1f} Z" fill="{color}" stroke="white" stroke-width="2"/>'
                    start += angle

                legend = ""
                for _, row in chart_data.iterrows():
                    pct = round(row["Nombre"] / total_chart * 100)
                    color = color_map.get(row["Statut"], "#6b7280")
                    legend += f"""<div style='display:flex;align-items:center;gap:8px;margin-bottom:8px;font-size:13px;'>
                        <div style='width:12px;height:12px;border-radius:50%;background:{color};flex-shrink:0;'></div>
                        <span style='color:#555;flex:1;'>{row["Statut"]}</span>
                        <span style='font-weight:700;'>{pct}%</span>
                        <span style='color:#6b7280;'>({row["Nombre"]})</span>
                    </div>"""

                st.markdown(f"""
                <div style='text-align:center;'>
                <svg viewBox='0 0 200 200' width='180' xmlns='http://www.w3.org/2000/svg'>
                {paths}
                <circle cx='100' cy='100' r='50' fill='white'/>
                <text x='100' y='96' text-anchor='middle' font-size='14' font-weight='800' fill='#111'>{total_chart}</text>
                <text x='100' y='112' text-anchor='middle' font-size='9' fill='#6b7280'>TOTAL</text>
                </svg>
                </div>
                <div style='margin-top:12px;'>{legend}</div>
                <div style='background:white;border-radius:12px;padding:14px;border:1px solid #e5e7eb;font-size:13px;margin-top:12px;'>
                    <div style='font-weight:700;color:#111;margin-bottom:8px;'>Résumé — {date_choisie}</div>
                    <div style='display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #f3f4f6;'><span style='color:#6b7280;'>Total filtré</span><span style='font-weight:600;'>{len(df_f)}</span></div>
                    <div style='display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #f3f4f6;'><span style='color:#d97706;'>En cours</span><span style='font-weight:600;'>{len(df_f[df_f["statut"]=="PENDING"])}</span></div>
                    <div style='display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #f3f4f6;'><span style='color:#059669;'>Livrés</span><span style='font-weight:600;'>{len(df_f[df_f["statut"]=="DELIVERED"])}</span></div>
                    <div style='display:flex;justify-content:space-between;padding:5px 0;'><span style='color:#dc2626;'>Erreurs</span><span style='font-weight:600;'>{len(df_f[df_f["statut"]=="ERREUR"])}</span></div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    # ── TAB 2: ENVOI SMS ──────────────────────────────────────────
    with tabs[1]:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📤 Envoi SMS Manuel</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-sub'>Envoyez un SMS directement depuis le dashboard</div>", unsafe_allow_html=True)

        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            phone_input = st.text_input("📱 Numéro de téléphone", placeholder="Ex: 0612345678")
            contrat_input = st.text_input("📄 Numéro de contrat", placeholder="Ex: CTR-001")
            montant_input = st.text_input("💰 Montant (DH)", placeholder="Ex: 1500")
            message_input = st.text_area(
                "✉️ Message",
                value="Madame, Monsieur, Votre facture {contrat} est impayee. La SRM-MS vous offre la possibilite d'echelonner le montant. Veuillez vous rendre a l'agence commerciale la plus proche.",
                height=120
            )
            if st.button("📤 Envoyer le SMS", use_container_width=True, key="send_sms"):
                if not phone_input or not contrat_input:
                    st.error("❌ Veuillez remplir le numéro et le contrat")
                else:
                    phone_clean = phone_input.strip()
                    phone_intl = "+212" + phone_clean[1:] if phone_clean.startswith("0") else phone_clean
                    msg = message_input.replace("{contrat}", contrat_input)
                    with st.spinner("Envoi en cours..."):
                        result = send_single_sms(phone_intl, msg)
                    if result["success"]:
                        st.success(f"✅ SMS envoyé! Statut: {result['statut']}")
                        log_sms(phone_intl, contrat_input, montant_input, msg, result["statut"], result["message_id"])
                    else:
                        st.error("❌ Échec de l'envoi.")
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown("""
            <div class='card'>
                <div style='font-size:1rem;font-weight:700;color:#111;margin-bottom:16px;'>💡 Guide</div>
                <div style='font-size:13px;color:#555;line-height:1.9;'>
                    <strong>Format numéro</strong><br>06XXXXXXXX ou 07XXXXXXXX<br><br>
                    <strong>Variable message</strong><br>Utilisez <code>{contrat}</code> pour insérer le numéro de contrat.<br><br>
                    <strong>Confirmation</strong><br>Le SMS est automatiquement enregistré dans l'historique.
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── TAB 3: HISTORIQUE ────────────────────────────────────────
    with tabs[2]:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📋 Historique complet</div>", unsafe_allow_html=True)
        if df.empty:
            st.info("Aucun SMS dans l'historique.")
        else:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df_hist = df.copy()
            df_hist["timestamp"] = df_hist["timestamp"].dt.strftime("%d/%m/%Y %H:%M")
            df_hist = df_hist.rename(columns={"timestamp":"Date","phone":"Téléphone","contrat":"Contrat","montant":"Montant (DH)","statut":"Statut"})
            cols_show = ["Date","Téléphone","Contrat","Montant (DH)","Statut"]
            st.dataframe(df_hist[cols_show], use_container_width=True, height=500)
            csv = df_hist.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Exporter CSV", csv, "historique_sms.csv", "text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── TAB 4: PARAMÈTRES ───────────────────────────────────────
    with tabs[3]:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>⚙️ Paramètres</div>", unsafe_allow_html=True)
        settings = load_settings()
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            jour1 = st.number_input("Jour 1 du mois", min_value=1, max_value=28, value=int(settings.get("jour1", 1)))
            jour2 = st.number_input("Jour 2 du mois", min_value=1, max_value=28, value=int(settings.get("jour2", 5)))
            heure = st.number_input("Heure d'envoi (GMT+1)", min_value=0, max_value=23, value=int(settings.get("heure", 9)))
            if st.button("💾 Sauvegarder", use_container_width=True, key="save_settings"):
                save_settings({"jour1": int(jour1), "jour2": int(jour2), "heure": int(heure)})
                st.success(f"✅ Envois les jours {int(jour1)} et {int(jour2)} à {int(heure)}h00")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class='card'>
                <div style='font-weight:700;color:#111;margin-bottom:12px;'>📌 Config actuelle</div>
                <div style='font-size:14px;color:#555;line-height:2;'>
                    Jour 1 : {settings.get('jour1', 1)} du mois<br>
                    Jour 2 : {settings.get('jour2', 5)} du mois<br>
                    Heure : {settings.get('heure', 9)}h00 (GMT+1)
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    show_footer()

# ══════════════════════════════════════════════════════════════════
# PAGE CLIENT
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "client":
    show_topbar()
    show_navbar()
    st.markdown(f"""
    <div class='hero' style="background: linear-gradient(135deg, rgba(0,0,0,0.65), rgba(0,0,0,0.4)), {bg2} center/cover no-repeat; background-size:cover !important;">
        <div class='hero-badge'>Espace Client</div>
        <div class='hero-title'>Consultez vos factures impayées</div>
        <div class='hero-desc'>Entrez votre numéro de téléphone ou numéro de contrat.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🔍 Consulter votre situation</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Recherchez par numéro de téléphone ou numéro de contrat</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.8, 1])
    with c2:
        recherche = st.text_input("Numéro ou contrat", placeholder="Ex: 0612345678 ou N20071207")
        chercher = st.button("🔍 Rechercher", use_container_width=True)

        if chercher and recherche.strip():
            from utils.db import load_sms_log
            df_client = load_sms_log()
            if not df_client.empty:
                r = recherche.strip()
                r_intl = "+212" + r[1:] if r.startswith("0") else r
                masque = (
                    df_client["phone"].astype(str).str.contains(re.escape(r), case=False, na=False) |
                    df_client["phone"].astype(str).str.contains(re.escape(r_intl), case=False, na=False) |
                    df_client["contrat"].astype(str).str.contains(re.escape(r), case=False, na=False)
                )
                resultats = df_client[masque].drop_duplicates(subset=["contrat"])
                if resultats.empty:
                    st.success("✅ Aucune facture impayée trouvée.")
                else:
                    for _, row in resultats.iterrows():
                        statut = row["statut"]
                        badge = {"PENDING": "<span class='badge badge-pending'>⏳ En attente</span>", "DELIVERED": "<span class='badge badge-delivered'>✅ Notifié</span>"}.get(statut, "<span class='badge badge-erreur'>❌ Erreur</span>")
                        st.markdown(f"""
                        <div class='card' style='margin-top:16px;'>
                            <div style='font-weight:700;color:#111;margin-bottom:16px;border-bottom:1px solid #f0fdf4;padding-bottom:12px;'>📄 Détail facture</div>
                            <div style='display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #f9fafb;font-size:14px;'><span style='color:#6b7280;'>Contrat</span><span style='font-weight:600;'>{row['contrat']}</span></div>
                            <div style='display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #f9fafb;font-size:14px;'><span style='color:#6b7280;'>Montant impayé</span><span style='font-weight:800;color:#dc2626;font-size:1.1rem;'>{row['montant']} DH</span></div>
                            <div style='display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #f9fafb;font-size:14px;'><span style='color:#6b7280;'>Téléphone</span><span style='font-weight:600;'>{row['phone']}</span></div>
                            <div style='display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #f9fafb;font-size:14px;'><span style='color:#6b7280;'>Date</span><span style='font-weight:600;'>{row['timestamp']}</span></div>
                            <div style='display:flex;justify-content:space-between;padding:10px 0;font-size:14px;'><span style='color:#6b7280;'>Statut</span>{badge}</div>
                            <div style='margin-top:16px;padding:14px;background:#f0fdf4;border-radius:10px;font-size:13px;color:#166534;border:1px solid #bbf7d0;'>
                                💡 Pour régulariser, rendez-vous à l'agence ou appelez le <strong>080 200 123</strong>.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("Aucune donnée disponible.")

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if st.button("← Retour", use_container_width=True, key="back_client"):
            st.session_state.page = "home"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    show_footer()

# ══════════════════════════════════════════════════════════════════
# PAGE QUI SOMMES-NOUS
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "qui_sommes":
    show_topbar()
    show_navbar("qui_sommes")
    st.markdown(f"""
    <div class='hero'>
        <div class='hero-badge'>À propos</div>
        <div class='hero-title'>Qui sommes-nous ?</div>
        <div class='hero-desc'>La SRM Marrakech-Safi, au service de millions d'habitants.</div>
    </div>
    <div class='section section-bg'>
        <div class='section-title'>Notre mission</div>
        <div class='section-sub'>Assurer des services publics essentiels de qualité</div>
        <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:20px;'>
            <div class='card'><div style='font-size:2rem;margin-bottom:12px;'>💧</div><div style='font-weight:700;color:#111;margin-bottom:8px;'>Distribution eau potable</div><div style='font-size:13px;color:#6b7280;line-height:1.7;'>Assurer l'accès à l'eau potable pour tous les habitants.</div></div>
            <div class='card'><div style='font-size:2rem;margin-bottom:12px;'>⚡</div><div style='font-weight:700;color:#111;margin-bottom:8px;'>Gestion électricité</div><div style='font-size:13px;color:#6b7280;line-height:1.7;'>Distribution et gestion du réseau électrique.</div></div>
            <div class='card'><div style='font-size:2rem;margin-bottom:12px;'>🔄</div><div style='font-weight:700;color:#111;margin-bottom:8px;'>Assainissement</div><div style='font-size:13px;color:#6b7280;line-height:1.7;'>Gestion du réseau d'assainissement liquide.</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    show_footer()

# ══════════════════════════════════════════════════════════════════
# PAGE PUBLICATIONS
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "publications":
    show_topbar()
    show_navbar("publications")
    st.markdown("""
    <div class='hero'>
        <div class='hero-badge'>Publications</div>
        <div class='hero-title'>Actualités & Conseils</div>
        <div class='hero-desc'>Retrouvez nos conseils et informations utiles.</div>
    </div>
    <div class='section'>
        <div class='section-title'>Nos publications</div>
        <div class='section-sub'>Conseils et informations pour nos clients</div>
        <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:20px;'>
            <div class='pub-card'><div class='pub-icon'>💡</div><div class='pub-title'>Régularisez vos factures</div><div class='pub-desc'>La SRM-MS vous offre la possibilité d'échelonner le paiement de vos factures.</div><div style='margin-top:12px;font-size:11px;color:#9ca3af;'>19 Avril 2026</div></div>
            <div class='pub-card'><div class='pub-icon'>📱</div><div class='pub-title'>Relance par SMS</div><div class='pub-desc'>Notre système de relance automatique par SMS vous notifie en cas de facture impayée.</div><div style='margin-top:12px;font-size:11px;color:#9ca3af;'>15 Avril 2026</div></div>
            <div class='pub-card'><div class='pub-icon'>🏢</div><div class='pub-title'>Nos agences sont ouvertes</div><div class='pub-desc'>Retrouvez nos agences ouvertes du lundi au vendredi de 8h à 17h.</div><div style='margin-top:12px;font-size:11px;color:#9ca3af;'>10 Avril 2026</div></div>
            <div class='pub-card'><div class='pub-icon'>💧</div><div class='pub-title'>Économisez l'eau</div><div class='pub-desc'>Adoptez les bons gestes pour économiser l'eau au quotidien.</div><div style='margin-top:12px;font-size:11px;color:#9ca3af;'>5 Avril 2026</div></div>
            <div class='pub-card'><div class='pub-icon'>⚡</div><div class='pub-title'>Sécurité électrique</div><div class='pub-desc'>Quelques conseils essentiels pour utiliser l'électricité en toute sécurité.</div><div style='margin-top:12px;font-size:11px;color:#9ca3af;'>1 Avril 2026</div></div>
            <div class='pub-card'><div class='pub-icon'>📊</div><div class='pub-title'>Rapport annuel 2024</div><div class='pub-desc'>Découvrez le bilan de notre première année d'activité.</div><div style='margin-top:12px;font-size:11px;color:#9ca3af;'>28 Mars 2026</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    show_footer()

# ══════════════════════════════════════════════════════════════════
# PAGE CONTACT
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "contact":
    show_topbar()
    show_navbar("contact")
    st.markdown("""
    <div class='hero'>
        <div class='hero-badge'>Contact</div>
        <div class='hero-title'>Contactez-nous</div>
        <div class='hero-desc'>Notre équipe est disponible pour répondre à vos questions.</div>
    </div>
    <div class='section section-bg'>
        <div class='section-title'>Nos coordonnées</div>
        <div class='section-sub'>Plusieurs moyens pour nous joindre</div>
        <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:20px;'>
            <div class='card' style='text-align:center;'><div style='font-size:2.5rem;margin-bottom:16px;'>📞</div><div style='font-weight:700;font-size:15px;color:#111;margin-bottom:8px;'>Téléphone</div><div style='font-size:13px;color:#6b7280;margin-bottom:16px;'>Lun/Ven 8h-17h</div><div style='background:#f0fdf4;border-radius:10px;padding:12px;font-weight:800;color:#166534;font-size:1.1rem;'>080 200 123</div></div>
            <div class='card' style='text-align:center;'><div style='font-size:2.5rem;margin-bottom:16px;'>✉️</div><div style='font-weight:700;font-size:15px;color:#111;margin-bottom:8px;'>Email</div><div style='font-size:13px;color:#6b7280;margin-bottom:16px;'>Réponse sous 24h</div><div style='background:#f0fdf4;border-radius:10px;padding:12px;font-weight:700;color:#166534;font-size:13px;'>service.client@srm-ms.ma</div></div>
            <div class='card' style='text-align:center;'><div style='font-size:2.5rem;margin-bottom:16px;'>📍</div><div style='font-weight:700;font-size:15px;color:#111;margin-bottom:8px;'>Siège social</div><div style='font-size:13px;color:#6b7280;margin-bottom:16px;'>Venez nous rendre visite</div><div style='background:#f0fdf4;border-radius:10px;padding:12px;font-weight:700;color:#166534;font-size:13px;'>Avenue Mohamed VI<br>Marrakech 40000</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    show_footer()