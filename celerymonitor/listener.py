from celery.events import EventReceiver
from celery.messaging import establish_connection

from celerymonitor.state import monitor_state


class EventListener(object):
    """Capture events sent by messages and store them in memory."""

    def __init__(self, state=monitor_state):
        self.state = state
        self.connection = establish_connection()
        self.receiver = EventReceiver(self.connection, handlers={
            "task-received": state.receive_task_received,
            "task-accepted": state.receive_task_event,
            "task-succeeded": state.receive_task_event,
            "task-retried": state.receive_task_event,
            "task-failed": state.receive_task_event,
            "worker-online": state.receive_worker_event,
            "worker-offline": state.receive_worker_event,
            "worker-heartbeat": state.receive_heartbeat,
        })

    def start(self):
        self.receiver.capture()
