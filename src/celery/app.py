from celery import Celery

celery_app = Celery('tasks',
                    # broker='redis://127.0.0.1:6379/3',
                    # backend='redis://127.0.0.1:6379/4')
                    broker='redis://dbserver:6379/3',
                    backend='redis://dbserver:6379/4')


celery_app.conf.beat_schedule = {
    # 'start-tg_bot-1-time': {
    #     'task': 'src.celery.tasks.start_bot_task',
    #     'schedule': 70,
    #     # 'schedule': crontab(month_of_year=datetime.now().month, day_of_month=datetime.now().day, hour=datetime.now().hour, minute=datetime.now().minute+1)
    # },
    'send_notification_every_minute': {
        'task': 'src.celery.tasks.send_notification',
        'schedule': 60,
    }
}


