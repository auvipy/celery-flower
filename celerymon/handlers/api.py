from __future__ import absolute_import

from functools import wraps

import anyjson
from tornado.web import RequestHandler, HTTPError

from celery import states
from celery.task.control import revoke
from celery.events.state import state


def JSON(fun):

    @wraps(fun)
    def _write_json(self, *args, **kwargs):
        content = fun(self, *args, **kwargs)
        self.write(anyjson.serialize(content))

    return _write_json


class APIHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        super(APIHandler, self).__init__(*args, **kwargs)
        self.set_header('Content-Type', 'application/javascript')


def api_handler(fun):

    @JSON
    def get(self, *args, **kwargs):
        return fun(self, *args, **kwargs)

    return type(fun.__name__, (APIHandler, ), {'get': get})


@api_handler
def task_state(request, task_id):
    try:
        task = state.tasks[task_id.strip('/')]
    except KeyError:
        raise HTTPError(404, 'Unknown task: %s' % task_id)
    if task.state in states.EXCEPTION_STATES:
        return task.info(extra=['traceback'])
    return task.info()


@api_handler
def list_tasks(request):
    limit = request.get_argument('limit', None)
    limit = limit and int(limit) or None

    since = request.get_argument('since', None)
    since = since and int(since) or None

    if not since:
        return state.tasks_by_timestamp(limit=limit)
    else:
        tasks = state.tasks_by_timestamp(limit=limit)
        if not tasks:
            return []
        tasks_since = []
        for task in tasks:
            id, data = task
            if data.timestamp > since:
                tasks_since.append(task)
            else:
                return tasks_since
        return tasks_since


@api_handler
def list_tasks_by_name(request, name):
    limit = request.get_argument('limit', None)
    limit = limit and int(limit) or None
    return state.tasks_by_type(name, limit=limit)


@api_handler
def list_task_types(request):
    return state.task_types()


@api_handler
def list_workers(request):
    return state.alive_workers()


@api_handler
def show_worker(request, node_name):
    try:
        return state.workers[node_name]
    except KeyError:
        raise HTTPError(404, 'Unknown worker node: %s' % node_name)


@api_handler
def list_worker_tasks(request, hostname):
    limit = request.get_argument('limit', None)
    limit = limit and int(limit) or None
    return state.tasks_by_worker(hostname, limit=limit)


class RevokeTaskHandler(APIHandler):
    SUPPORTED_METHODS = ['POST']

    @JSON
    def post(self):
        task_id = self.get_argument('task_id')
        revoke(task_id)
        return {'ok': True}
