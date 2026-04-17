import streamlit as st
import pandas as pd
import json
import os
import time

LOG_FILE = "data/sms_log.json"

st.set_page_config(page_title="SRM-CS Dashboard", layout="wide")

# ─── STYLE SRM ───────────────────────────────────────────
st.markdown("""
<style>
body { margin:0; }

/* TOP BAR */
.topbar {
    background:#3b8dbd;
    color:white;
    padding:8px 30px;
    font-size:14px;
}

/* HEADER */
.header {
    background:white;
    padding:15px 30px;
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.logo {
    font-size:22px;
    font-weight:bold;
    color:#3b8dbd;
}

/* NAVBAR */
.nav {
    background:#3b8dbd;
    padding:10px 30px;
}
.nav span {
    color:white;
    margin-right:25px;
    font-weight:500;
}

/* HERO IMAGE */
.hero {
    background-image: url("https://images.unsplash.com/photo-1597211684565-dca64d51f8c5");
    background-size:cover;
    background-position:center;
    height:300px;
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-size:32px;
    font-weight:bold;
}

/* CARDS */
.card {
    background:white;
    padding:20px;
    border-radius:10px;
    text-align:center;
    box-shadow:0 5px 15px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ─── TOPBAR ───────────────────────────────────────────────
st.markdown("""
<div class="topbar">
✉️ contact@srm-cs.ma &nbsp;&nbsp;&nbsp; 📞 (+212) 522 31 20 20
</div>
""", unsafe_allow_html=True)

# ─── HEADER ───────────────────────────────────────────────
st.markdown("""
<div class="header">
<div class="logo">💧 SRM-CS</div>
<div>
👤 Centre Client | 👥 +130000 Clients | 📍 Marrakech-Safi
</div>
</div>
""", unsafe_allow_html=True)

# ─── NAVBAR ───────────────────────────────────────────────
st.markdown("""
<div class="nav">
<span>Accueil</span>
<span>Dashboard</span>
<span>SMS</span>
<span>Rapports</span>
</div>
""", unsafe_allow_html=True)

# ─── LOGIN ────────────────────────────────────────────────
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
            st.error("Wrong login")

    st.stop()

# ─── HERO (IMAGE MARRAKECH) ──────────────────────────────
st.markdown("""
<div class="hero">
Gestion des SMS - Marrakech
</div>
""", unsafe_allow_html=True)

# ─── DATA ────────────────────────────────────────────────
if not os.path.exists(LOG_FILE):
    st.warning("No data")
    st.stop()

with open(LOG_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date

# ─── FILTER DATE ─────────────────────────────────────────
date = st.date_input("📅 Choisir date", value=df["date"].max())
df = df[df["date"] == date]

# ─── METRICS ─────────────────────────────────────────────
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

# ─── TABLE ───────────────────────────────────────────────
st.subheader("📋 SMS envoyés")
st.dataframe(df, use_container_width=True)

# ─── CHART ───────────────────────────────────────────────
st.subheader("📊 Statut")
st.bar_chart(df["statut"].value_counts())