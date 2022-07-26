FROM python:3.9.10-alpine

RUN adduser -D weather

WORKDIR /home/weather
ENV PYTHONPATH "${PYTHONPATH}:/home/weather"

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN pip install -r requirements.txt

COPY src src

USER weather
EXPOSE 5000

CMD sleep 5 && celery -A src.celery.tasks worker --loglevel=INFO --beat

