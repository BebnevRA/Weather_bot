from celery import Celery
from celery.schedules import crontab

celery_app = Celery('tasks',
                    broker='redis://127.0.0.1:6379/3',
                    backend='redis://127.0.0.1:6379/4')


celery_app.conf.beat_schedule = {
    'start-tg_bot-1-time': {
        'task': 'src.celery.tasks.start_bot_task',
        'schedule': crontab(minute="*/100"),
        # 'schedule': crontab(hour=7, minute=30, day_of_week=1)
    },
    # 'add-every-30-seconds': {
    #         'task': 'tasks.add',
    #         'schedule': 30.0,
    #         'args': (16, 16)
    # },
}
