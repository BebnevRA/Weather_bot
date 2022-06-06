FROM python:3.9.10-alpine

RUN adduser -D weather

WORKDIR /home/weather

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN pip install -r requirements.txt

COPY src src

USER weather
EXPOSE 5000
CMD celery -A src.celery.tasks worker --loglevel=INFO --beat
