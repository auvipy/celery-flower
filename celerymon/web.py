from __future__ import absolute_import

import os
import threading

from tornado import httpserver
from tornado import ioloop
from tornado.web import Application, StaticFileHandler

from .handlers import api, main


class WebServerThread(threading.Thread):

    def __init__(self, port=8989, address=''):
        super(WebServerThread, self).__init__()
        self.port = port
        self.address = address
        self.setDaemon(True)

    def run(self):
        settings = {
            'template_path': os.path.join(
                os.path.dirname(__file__), 'templates'
            )
        }

        app = Application([

            # API Endpoints
            (r'/api/?$', main.api_detail),
            (r'/api/task/name/?$', api.list_task_types),
            (r'/api/task/name/(.+?)/?', api.list_tasks_by_name),
            (r'/api/task/?', api.list_tasks),
            (r'/api/revoke/task/', api.RevokeTaskHandler),
            (r'/api/task/(.+)/?', api.task_state),
            (r'/api/worker/', api.list_workers),
            (r'/api/worker/(.+?)/tasks/?', api.list_worker_tasks),
            (r'/api/worker/(.+?)/?', api.show_worker),

            # Static Files
            (r'/static/(.*)', StaticFileHandler, {
                'path': os.path.join(os.path.dirname(__file__), 'static'),
            }),

            # Web UI Endpoints
            (r'/$', main.index),

        ], **settings)

        http_server = httpserver.HTTPServer(app)
        http_server.listen(self.port, address=self.address)
        ioloop.IOLoop.instance().start()
