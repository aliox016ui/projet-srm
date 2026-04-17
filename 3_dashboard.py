import streamlit as st
import pandas as pd
import json
import os

LOG_FILE = "data/sms_log.json"

st.set_page_config(page_title="SRM - Suivi SMS", page_icon="📊", layout="wide")

# ── Authentication ─────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 SRM — Connexion")
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("👤 Nom d'utilisateur")
        password = st.text_input("🔑 Mot de passe", type="password")
        if st.button("Se connecter", use_container_width=True):
            if username == "srm" and password == "srm2024":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect")
    st.stop()

# ── Dashboard ──────────────────────────────────────────────────────
st.title("📊 SRM — Tableau de bord SMS")

if st.button("🚪 Déconnexion"):
    st.session_state.logged_in = False
    st.rerun()

if not os.path.exists(LOG_FILE):
    st.info("Aucun SMS envoye pour le moment.")
    st.stop()

with open(LOG_FILE, "r", encoding="utf-8") as f:
    log = json.load(f)

df = pd.DataFrame(log)

total   = len(df)
pending = len(df[df["statut"] == "PENDING"])
livre   = len(df[df["statut"] == "DELIVERED"])
erreur  = len(df[df["statut"] == "ERREUR"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("📨 Total",     total)
col2.metric("⏳ En cours",  pending)
col3.metric("✅ Livres",    livre)
col4.metric("❌ Erreurs",   erreur)

st.divider()

statuts = ["Tous"] + sorted(df["statut"].unique().tolist())
choix   = st.selectbox("Filtrer par statut", statuts)

df_affiche = df if choix == "Tous" else df[df["statut"] == choix]

st.dataframe(
    df_affiche[["timestamp", "phone", "contrat", "montant", "statut"]],
    use_container_width=True
)

st.subheader("Repartition des statuts")
st.bar_chart(df["statut"].value_counts())
