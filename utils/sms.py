import requests
import os

def send_single_sms(phone, message):
    api_key = os.getenv("INFOBIP_API_KEY")
    base_url = os.getenv("INFOBIP_BASE_URL")
    sender = os.getenv("SENDER", "SRM")

    headers = {
        "Authorization": f"App {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "messages": [{
            "from": sender,
            "destinations": [{"to": phone}],
            "text": message
        }]
    }
    try:
        r = requests.post(
            f"{base_url}/sms/2/text/advanced",
            json=payload, headers=headers, timeout=10
        )
        r.raise_for_status()
        data = r.json()
        statut = data["messages"][0]["status"]["groupName"]
        msg_id = data["messages"][0]["messageId"]
        return {"success": True, "statut": statut, "message_id": msg_id}
    except Exception as e:
        return {"success": False, "statut": "ERREUR", "message_id": ""}