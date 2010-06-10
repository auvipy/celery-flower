from celery.events import EventReceiver
from celery.messaging import establish_connection

from celery.events.state import state


class EventListener(object):
    """Capture events sent by messages and store them in memory."""

    def __init__(self, state=state):
        self.state = state
        self.connection = establish_connection()
        self.receiver = EventReceiver(self.connection,
                                      handlers={"*": self.state.event})

    def start(self):
        self.receiver.capture()
