# tasks.py
from celery import Celery
import database_func
from celery.utils.log import get_task_logger

# Настройка Celery
celery = Celery(__name__)
celery.conf.broker_url = 'redis://localhost:6379/0'
celery.conf.result_backend = 'redis://localhost:6379/0'
celery.conf.beat_schedule = {
    'delete-old-vacancies-every-3-hours': {
        'task': 'tasks.delete_old_vacancies_task',
        'schedule': 30.0,  # 3 часа в секундах
    },
}

celery.conf.timezone = 'UTC'

logger = get_task_logger(__name__)

@celery.task()
def delete_old_vacancies_task():
    logger.info('OK=1======\nOK=1======\nOK=1======\nOK=1======\nOK=1======\n')
    database_func.delete_old_vacancies()
    logger.info('OK=2======\nOK=2======\nOK=2======\nOK=2======\nOK=2======\n')
