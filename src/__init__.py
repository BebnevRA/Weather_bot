import redis

from src.db_schedule import DBSchedule

db_check_ip = redis.Redis(host='redis_db', port=6379, db=0)
db_ban_list = redis.Redis(host='redis_db', port=6379, db=1)

db_schedule = DBSchedule(user='postgres', port='5432',
                         password='0455', host='postgres_db')
