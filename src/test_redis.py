import datetime

import redis


if __name__ == '__main__':
    COUNTFORBAN = 5
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)

    # now = datetime.datetime.utcnow()
    # username = 'etroks'
    #
    # username_min = f'{username}-{now.minute}'
    # count = r.incr(username_min)
    # if count < COUNTFORBAN:
    #     print(r.expire(username_min, 60))
    # else:
    #     print('BAN ' + username)




    # username = '12345'
    # now = datetime.datetime.utcnow()
    # time = f'{now.minute}.{now.second}'
    #
    # r.lpush(username, time)
    # if r.llen(username) == COUNTFORBAN:
    #     delta = float(r.lindex(username, 0)) - float(r.lindex(username, -1))
    #
    #     if delta < -59 or delta < 1:
    #         print('BAN')
    #     else:
    #         r.rpop(username)
    #         print('OK')
    print(r.set('55', 'kik'))
    print(r.get('56'))

