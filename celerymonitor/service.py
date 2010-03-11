from celerymonitor.web import WebServerThread
from celerymonitor.listener import EventListener


class MonitorService(object):
    """celerymon"""

    def __init__(self, logger, http_port=8989):
        self.logger = logger
        self.http_port = http_port

    def start(self):
        WebServerThread(port=self.http_port).start()
        EventListener().start()
