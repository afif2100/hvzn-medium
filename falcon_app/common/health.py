import falcon
from datetime import datetime
from common.base_logger import BaseLogger

log = BaseLogger(__name__)


class HealthCheck(object):

    def __init__(self):
        self.start_time = datetime.now()

    def health(self):
        """
        Function that give health status
        """
        now_time = datetime.now()
        delta_time = now_time - self.start_time

        return {"message": "ok",
                "uptime": str(delta_time)}

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = self.health()
