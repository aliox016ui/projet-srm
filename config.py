# config.py
from dotenv import load_dotenv
import os

load_dotenv()

INFOBIP_API_KEY   = os.getenv("INFOBIP_API_KEY")
INFOBIP_BASE_URL  = os.getenv("INFOBIP_BASE_URL")
SENDER            = os.getenv("SENDER")
INPUT_FILE        = os.getenv("INPUT_FILE")
FILTERED_FILE     = os.getenv("FILTERED_FILE")
LOG_FILE          = os.getenv("LOG_FILE")