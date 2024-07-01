from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from database_func import delete_old_vacancies

def delete_task():
    delete_old_vacancies()

scheduler = BackgroundScheduler()
scheduler.add_job(delete_task, 'interval', hours=2)
