import logging
import time
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from send_sms import send_sms_campaign
from filter import run_filter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

def run_full_campaign():
    log.info(">>> Démarrage campagne automatique")
    try:
        run_filter()
        send_sms_campaign()
        log.info(">>> Campagne terminée avec succès")
    except Exception as e:
        log.error(f">>> Erreur campagne: {e}")

scheduler = BlockingScheduler(timezone="Africa/Casablanca")

# Jour 1 et jour 15 de chaque mois à 09:00
scheduler.add_job(
    run_full_campaign,
    CronTrigger(day="1,15", hour=9, minute=0),
    id="sms_campaign",
    name="Campagne SMS SRM",
    replace_existing=True
)

log.info("Scheduler démarré — campagnes: jour 1 et 15 à 09:00")
log.info("Prochain envoi: " + str(
    scheduler.get_jobs()[0].next_run_time
))

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    log.info("Scheduler arrêté")