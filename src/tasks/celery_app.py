from celery import Celery
from src.config import settings

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=["src.tasks.tasks"],
)


celery_instance.conf.broker_connection_retry_on_startup = True

celery_instance.conf.beat_schedule = {
    "luboe-nazvanie": {
        "task": "booking_today_checkin",
        "schedule": 5,
    }
}
