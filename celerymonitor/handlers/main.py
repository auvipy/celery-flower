import os

from tornado.web import RequestHandler, Application, HTTPError


def T(name):
    return os.path.join(os.pardir, "templates", "%s.html" % name)


def handler(fun):

    def get(self, *args, **kwargs):
        return fun(self, *args, **kwargs)

    return type(fun.__name__, (RequestHandler, ), {"get": get})



@handler
def index(request):
    return request.render(T("index"))



MAIN = [
        (r"/$", index),
]




