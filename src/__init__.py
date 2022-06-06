import os

import redis

from src.db_schedule1 import DBSchedule

# db_check_ip = redis.Redis(host='127.0.0.1', port=6379, db=0)
# db_ban_list = redis.Redis(host='127.0.0.1', port=6379, db=1)
db_check_ip = redis.Redis(host='dbserver', port=6379, db=0)
db_ban_list = redis.Redis(host='dbserver', port=6379, db=1)

db_schedule = DBSchedule(os.path.dirname(os.path.abspath(__file__)) + '/sqlite_python.db')

