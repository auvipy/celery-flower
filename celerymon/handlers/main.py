from __future__ import absolute_import

from tornado.web import RequestHandler


def handler(fun):

    def get(self, *args, **kwargs):
        return fun(self, *args, **kwargs)

    return type(fun.__name__, (RequestHandler, ), {'get': get})


@handler
def index(request):
    return request.render('index.html', title='Celery Monitor')


@handler
def api_detail(request):
    return request.render('api_detail.html', title='API')
