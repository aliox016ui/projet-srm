import streamlit as st
import pandas as pd
import json
import os
from config import LOG_FILE

st.set_page_config(page_title="SRM - Suivi SMS", page_icon="📊", layout="wide")

st.title("📊 SRM — Tableau de bord SMS")

if not os.path.exists(LOG_FILE) or LOG_FILE is None:
    st.infost.info("Aucun SMS envoye pour le moment.")
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