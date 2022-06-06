Запуск redis:
docker run -d -p 6379:6379 redis
(docker exec -t ___ bash)

Запуск celery:
celery -A src.celery.tasks worker --loglevel=INFO --beat
(-l debug)

Запук бота:
python src/tg/handlers.py

