from __future__ import absolute_import

import os

from tornado.web import RequestHandler, StaticFileHandler
from tornado.template import Template

from celery import states
from celery.task.control import revoke
from celery.events.state import state


def handler(fun):

    def get(self, *args, **kwargs):
        return fun(self, *args, **kwargs)

    return type(fun.__name__, (RequestHandler, ), {"get": get})


@handler
def index(request):
    return request.render("index.html", title="Celerymon")

@handler
def api_detail(request):
    return request.render("api_detail.html", title = "API")
