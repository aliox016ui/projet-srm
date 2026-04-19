import pandas as pd
import requests
import json
import os
import logging
from datetime import datetime

from config import (
    INFOBIP_API_KEY, INFOBIP_BASE_URL, SENDER,
    FILTERED_FILE, LOG_FILE, SUPABASE_URL, SUPABASE_KEY
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

def get_supabase_client():
    if SUPABASE_URL and SUPABASE_KEY:
        from supabase import create_client
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    return None

def already_sent(supabase, phone, contrat):
    if not supabase:
        return False
    try:
        res = supabase.table("sms_log") \
            .select("id") \
            .eq("phone", phone) \
            .eq("contrat", str(contrat)) \
            .eq("statut", "PENDING") \
            .execute()
        return len(res.data) > 0
    except Exception as e:
        log.warning(f"Supabase check failed: {e}")
        return False

def send_sms_campaign():
    log.info("=== Démarrage campagne SMS ===")

    if not os.path.exists(FILTERED_FILE):
        log.error(f"Fichier filtré introuvable: {FILTERED_FILE}")
        return

    df = pd.read_csv(FILTERED_FILE, dtype={"phone": str})
    log.info(f"{len(df)} clients à contacter")

    supabase = get_supabase_client()

    headers = {
        "Authorization": f"App {INFOBIP_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    local_log = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            local_log = json.load(f)

    sent = 0
    skipped = 0
    errors = 0

    for _, row in df.iterrows():
        phone   = str(row["phone"])
        contrat = row["contrat"]
        montant = row["montant"]

        if already_sent(supabase, phone, contrat):
            log.info(f"[SKIP] {phone} — déjà notifié")
            skipped += 1
            continue

        message = (
            f"Madame, Monsieur, Votre facture {contrat} est impayee. "
            f"La SRM-CS vous offre la possibilite d'echelonner le montant. "
            f"Veuillez vous rendre a l'agence commerciale la plus proche."
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
                timeout=15
            )
            r.raise_for_status()
            reponse_api = r.json()
            statut  = reponse_api["messages"][0]["status"]["groupName"]
            msg_id  = reponse_api["messages"][0]["messageId"]
            log.info(f"[OK] {phone} | {contrat} | {statut}")
            sent += 1

        except requests.exceptions.RequestException as e:
            statut = "ERREUR"
            msg_id = ""
            log.error(f"[ERREUR] {phone} → {e}")
            errors += 1

        entry = {
            "timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "phone":      phone,
            "contrat":    str(contrat),
            "montant":    str(montant),
            "message":    message,
            "statut":     statut,
            "message_id": msg_id
        }
        local_log.append(entry)

        if supabase:
            try:
                supabase.table("sms_log").insert(entry).execute()
            except Exception as e:
                log.warning(f"Supabase insert failed: {e}")

    os.makedirs("data", exist_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(local_log, f, ensure_ascii=False, indent=2)

    log.info(f"=== Campagne terminée: {sent} envoyés, {skipped} ignorés, {errors} erreurs ===")

if __name__ == "__main__":
    send_sms_campaign()