import requests
import logging
from config import INFOBIP_API_KEY, INFOBIP_BASE_URL, SENDER

log = logging.getLogger(__name__)

def send_single_sms(phone: str, message: str) -> dict:
    headers = {
        "Authorization": f"App {INFOBIP_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
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
        data = r.json()
        statut = data["messages"][0]["status"]["groupName"]
        msg_id = data["messages"][0]["messageId"]
        return {"success": True, "statut": statut, "message_id": msg_id}
    except Exception as e:
        log.error(f"SMS error: {e}")
        return {"success": False, "statut": "ERREUR", "message_id": ""}