from celery import Celery

celery_app = Celery('tasks',
                    broker='redis://redis_db:6379/3',
                    backend='redis://redis_db:6379/4')


celery_app.conf.beat_schedule = {
    'send_notification_every_minute': {
        'task': 'src.celery.tasks.send_notification',
        'schedule': 60,
    }
}


