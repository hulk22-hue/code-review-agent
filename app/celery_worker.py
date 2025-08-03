# app/celery_worker.py

from celery import Celery
from app.utils.config import REDIS_URL

celery = Celery(
    "code_review_agent",
    broker=REDIS_URL,
    backend=REDIS_URL
)

import app.services.task_service