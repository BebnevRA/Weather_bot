import os
import datetime

TG_BOT_TOKEN = os.environ.get('TG_BOT_TOKEN') or 'secret key'
COUNT_FOR_BAN = 10
TIMEZONE_OFFSET = datetime.timezone(datetime.timedelta(hours=3))
