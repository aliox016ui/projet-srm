import pandas as pd
import requests
import json
import os
from datetime import datetime

from config import INFOBIP_API_KEY, INFOBIP_BASE_URL, SENDER, FILTERED_FILE, LOG_FILE

df = pd.read_csv(FILTERED_FILE, dtype={"phone": str})
print(f"[INFO] {len(df)} clients a contacter")

headers = {
    "Authorization": f"App {INFOBIP_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        log = json.load(f)
else:
    log = []

for _, row in df.iterrows():
    phone   = str(row["phone"])
    contrat = row["contrat"]
    montant = row["montant"]

    message = (
        f"Madame, Monsieur, Votre facture {contrat} est impayes. "
    f"La SRM-CS vous offre la possibilite d'echelonner le montant. "
    f"Veuillez vous rendre a l'agence commerciale la plus proche pour legaliser une demande de facilite."
)

    payload = {
        "messages": [{
            "from": SENDER,
            "destinations": [{"to": phone}],
            "text": message
        }]
    }

    try:
        r = requests.post(
            f"{INFOBIP_BASE_URL}/sms/2/text/advanced",
            json=payload,
            headers=headers,
            timeout=10
        )
        r.raise_for_status()

        reponse_api = r.json()
        statut      = reponse_api["messages"][0]["status"]["groupName"]
        msg_id      = reponse_api["messages"][0]["messageId"]

        print(f"[OK] {phone} | contrat {contrat} | statut: {statut}")

    except requests.exceptions.RequestException as e:
        statut = "ERREUR"
        msg_id = ""
        print(f"[ERREUR] {phone} -> {e}")

    log.append({
        "timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "phone":      phone,
        "contrat":    str(contrat),
        "montant":    str(montant),
        "message":    message,
        "statut":     statut,
        "message_id": msg_id
    })

os.makedirs("data", exist_ok=True)
with open(LOG_FILE, "w", encoding="utf-8") as f:
    json.dump(log, f, ensure_ascii=False, indent=2)

print(f"\n[OK] Log sauvegarde -> '{LOG_FILE}'")