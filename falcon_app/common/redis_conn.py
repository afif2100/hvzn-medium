import redis
from common.base_logger import BaseLogger

logger = BaseLogger('redis')


class RedisConnection(object):

    def __init__(self):
        self.host = "localhost"
        self.password = ""
        self.port = 6379

    def connectdb(self):
        self.red = redis.Redis(host=self.host,
                               port=self.port,
                               password=self.password)

    def check_connection(self):
        try:
            self.connectdb()
            self.red.ping()
            db_ok = True
        except Exception as e:
            logger.error(e)
            db_ok = False

        return db_ok
