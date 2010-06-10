from functools import wraps

import simplejson
from tornado.web import RequestHandler, Application

from celery import states
from celery.task.control import revoke

from celery.events.state import state


def JSON(fun):

    @wraps(fun)
    def _write_json(self, *args, **kwargs):
        content = fun(self, *args, **kwargs)
        self.write(simplejson.dumps(content))

    return _write_json


class APIHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        super(APIHandler, self).__init__(*args, **kwargs)
        self.set_header("Content-Type", "application/javascript")


def api_handler(fun):

    @JSON
    def get(self, *args, **kwargs):
        return fun(self, *args, **kwargs)

    return type(fun.__name__, (APIHandler, ), {"get": get})


@api_handler
def task_state(request, task_id):
    task = state.tasks[task_id]
    if task.state in states.EXCEPTION_STATES:
        return task.info(extra=["traceback"])
    return task.info()


@api_handler
def list_tasks(request):
    return state.tasks_by_timestamp()


@api_handler
def list_tasks_by_name(request, name):
    return state.tasks_by_type(name)


@api_handler
def list_task_types(request):
    return state.task_types()


@api_handler
def list_workers(request):
    return state.alive_workers()


@api_handler
def list_worker_tasks(request, hostname):
    return state.list_worker_tasks(hostname)


class RevokeTaskHandler(APIHandler):

    SUPPORTED_METHODS = ["POST"]

    @JSON
    def post(self):
        task_id = self.get_argument("task_id")
        revoke(task_id)
        return {"ok": True}


API = [
       (r"/task/name/$", list_task_types),
       (r"/task/name/(.+?)", list_tasks_by_name),
       (r"/task/$", list_tasks),
       (r"/revoke/task/", RevokeTaskHandler),
       (r"/task/(.+)", task_state),
       (r"/worker/", list_workers),
       (r"/worker/(.+?)/tasks", list_worker_tasks),
]
