from dotenv import load_dotenv
import os

load_dotenv()

INFOBIP_API_KEY   = os.getenv("INFOBIP_API_KEY")
INFOBIP_BASE_URL  = os.getenv("INFOBIP_BASE_URL")
SENDER            = os.getenv("SENDER", "SRM")
INPUT_FILE        = os.getenv("INPUT_FILE", "data/clients.xlsx")
FILTERED_FILE     = os.getenv("FILTERED_FILE", "data/clients_filtered.csv")
LOG_FILE          = os.getenv("LOG_FILE", "data/sms_log.json")
SUPABASE_URL      = os.getenv("SUPABASE_URL")
SUPABASE_KEY      = os.getenv("SUPABASE_KEY")