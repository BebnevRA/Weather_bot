docker run -d -p 6379:6379 redis
celery -A src.celery.tasks worker --loglevel=INFO --beat
from src.celery.tasks import wait, add, test_task, start_bot_task
