import streamlit as st
import pandas as pd
import json
import os
import time

# ─── CONFIG ─────────────────────────────────────────────
LOG_FILE = "data/sms_log.json"
LOGO_PATH = "logo.jpg"  # حط هنا اللوغو لي عطيتك

st.set_page_config(page_title="SRM-CS Dashboard", layout="wide")

# ─── STYLE ──────────────────────────────────────────────
st.markdown("""
<style>
.topbar {
    background:#3b8dbd;
    color:white;
    padding:8px 30px;
    font-size:14px;
}

.nav {
    background:#3b8dbd;
    padding:10px 30px;
}
.nav span {
    color:white;
    margin-right:25px;
    font-weight:500;
}

.card {
    background:white;
    padding:20px;
    border-radius:10px;
    text-align:center;
    box-shadow:0 5px 15px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ─── TOP BAR ────────────────────────────────────────────
st.markdown("""
<div class="topbar">
✉️ contact@srm-cs.ma &nbsp;&nbsp;&nbsp; 📞 (+212) 522 31 20 20
</div>
""", unsafe_allow_html=True)

# ─── HEADER (LOGO + INFO) ───────────────────────────────
col1, col2 = st.columns([1,3])

with col1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=180)

with col2:
    st.markdown("""
    <h2 style='color:#3b8dbd;'>Société Régionale Multiservices</h2>
    <p>👤 Centre Client | 👥 +130000 Clients | 📍 Marrakech-Safi</p>
    """, unsafe_allow_html=True)

# ─── NAVBAR ─────────────────────────────────────────────
st.markdown("""
<div class="nav">
<span>Accueil</span>
<span>Dashboard</span>
<span>SMS</span>
<span>Rapports</span>
</div>
""", unsafe_allow_html=True)

# ─── LOGIN ──────────────────────────────────────────────
if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    st.markdown("### 🔐 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "srm" and p == "srm2024":
            st.session_state.logged = True
            st.rerun()
        else:
            st.error("❌ Wrong login")

    st.stop()

# ─── IMAGE MARRAKECH (وسط الصفحة) ───────────────────────
st.markdown("""
<div style="
background-image: url('https://images.unsplash.com/photo-1548013146-72479768bada');
background-size: cover;
background-position: center;
height: 350px;
display:flex;
align-items:center;
justify-content:center;
color:white;
font-size:30px;
font-weight:bold;
">
🌴 Marrakech - Suivi SMS
</div>
""", unsafe_allow_html=True)

# ─── DATA ───────────────────────────────────────────────
if not os.path.exists(LOG_FILE):
    st.warning("No data yet")
    st.stop()

with open(LOG_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date

# ─── FILTRE DATE ────────────────────────────────────────
date = st.date_input("📅 Choisir date", value=df["date"].max())
df = df[df["date"] == date]

# ─── METRICS ────────────────────────────────────────────
total = len(df)
pending = len(df[df["statut"] == "PENDING"])
delivered = len(df[df["statut"] == "DELIVERED"])
error = len(df[df["statut"] == "ERREUR"])

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown(f'<div class="card"><h2>{total}</h2>Total</div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="card"><h2>{pending}</h2>Pending</div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="card"><h2>{delivered}</h2>Delivered</div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="card"><h2>{error}</h2>Error</div>', unsafe_allow_html=True)

# ─── TABLE ──────────────────────────────────────────────
st.subheader("📋 SMS envoyés")
st.dataframe(df, use_container_width=True)

# ─── CHART ──────────────────────────────────────────────
st.subheader("📊 Statut")
st.bar_chart(df["statut"].value_counts())