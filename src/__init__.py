import redis

# if __name__ == '__main__':
db_check_ip = redis.Redis(host='127.0.0.1', port=6379, db=0)
db_ban_list = redis.Redis(host='127.0.0.1', port=6379, db=1)



