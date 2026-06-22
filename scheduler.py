import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from main_tv import run_tv_agent

scheduler = BlockingScheduler(timezone="Asia/Tashkent")

scheduler.add_job(run_tv_agent, CronTrigger(hour=9, minute=0, timezone="Asia/Tashkent"))
scheduler.add_job(run_tv_agent, CronTrigger(hour=12, minute=0, timezone="Asia/Tashkent"))
scheduler.add_job(run_tv_agent, CronTrigger(hour=15, minute=0, timezone="Asia/Tashkent"))
scheduler.add_job(run_tv_agent, CronTrigger(hour=18, minute=0, timezone="Asia/Tashkent"))
scheduler.add_job(run_tv_agent, CronTrigger(hour=21, minute=0, timezone="Asia/Tashkent"))

print("🕐 Планировщик запущен. Выпуски в 09:00, 12:00, 15:00, 18:00, 21:00 (Ташкент)")
print("   Для остановки — Ctrl+C")

try:
    scheduler.start()
except KeyboardInterrupt:
    print("\nПланировщик остановлен.")
