from __future__ import absolute_import

from .consumer import EventConsumer
from .web import WebServerThread


class MonitorService(object):

    def __init__(self, logger, http_port=8989, http_address=''):
        self.logger = logger
        self.http_port = http_port
        self.http_address = http_address

    def start(self):
        WebServerThread(port=self.http_port,
                        address=self.http_address).start()
        EventConsumer().start()
