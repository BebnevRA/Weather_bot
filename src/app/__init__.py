import redis
from flask import Flask

app = Flask(__name__)

# вот тут дб поднимать
db_check_ip = redis.Redis(host='127.0.0.1', port=6379, db=0)
from src.app import routes
