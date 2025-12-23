from celery import Celery
import os

REDIS_URL = os.environ["REDIS_URL"]

celery = Celery(
    "webhook_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)
