from __future__ import absolute_import

from celery import current_app
from celery.events.state import state


class EventConsumer(object):
    """Capture events sent by messages and store them in memory."""

    def __init__(self, state=state):
        self.app = current_app
        self.state = state
        self.connection = self.app.broker_connection()
        self.receiver = self.app.events.Receiver(self.connection,
                                 handlers={'*': self.state.event})

    def start(self):
        self.receiver.capture()
