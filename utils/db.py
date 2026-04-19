import os
import json
import logging
from datetime import datetime

log = logging.getLogger(__name__)
SETTINGS_FILE = "data/settings.json"

def get_supabase():
    from config import SUPABASE_URL, SUPABASE_KEY
    if SUPABASE_URL and SUPABASE_KEY:
        from supabase import create_client
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    return None

def log_sms(phone, contrat, montant, message, statut, message_id):
    supabase = get_supabase()
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "phone": phone,
        "contrat": str(contrat),
        "montant": str(montant),
        "message": message,
        "statut": statut,
        "message_id": message_id
    }
    if supabase:
        try:
            supabase.table("sms_log").insert(entry).execute()
        except Exception as e:
            log.warning(f"Supabase insert failed: {e}")
    return entry

def load_sms_log():
    supabase = get_supabase()
    if supabase:
        try:
            resp = supabase.table("sms_log").select("*").order("timestamp", desc=True).execute()
            import pandas as pd
            return pd.DataFrame(resp.data) if resp.data else pd.DataFrame()
        except Exception as e:
            log.warning(f"Supabase load failed: {e}")
    import pandas as pd
    return pd.DataFrame()

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {"jour1": 1, "jour2": 5, "heure": 9}

def save_settings(settings: dict):
    os.makedirs("data", exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)