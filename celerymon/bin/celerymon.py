#!/usr/bin/env python
"""celerymon

.. program:: celerymon

.. cmdoption:: -P, --port

    Port the webserver should listen to. Default: ``8989``.

.. cmdoption:: -B, --bind

    Address the webserver should bind to. Default (any).

.. cmdoption:: -f, --logfile

    Path to log file. If no logfile is specified, ``stderr`` is used.

.. cmdoption:: -l, --loglevel

.. cmdoption:: -D, --detach

    Daemonize celerymon.

    Logging level, choose between ``DEBUG``, ``INFO``, ``WARNING``,
    ``ERROR``, ``CRITICAL``, or ``FATAL``.

"""
from __future__ import absolute_import
from __future__ import with_statement

import os
import sys

from celery.bin.base import Command, Option, daemon_options
from celery.platforms import (
    detached,
    set_process_title,
    strargv,
    create_pidlock,
)
from celery.utils import LOG_LEVELS

from .. import __version__
from ..service import MonitorService

STARTUP_INFO_FMT = """
Configuration ->
    . broker -> %(conninfo)s
    . webserver -> http://%(http_address)s:%(http_port)s
""".strip()

OPTION_LIST = (
)


class MonitorCommand(Command):
    namespace = 'celerymon'
    enable_config_from_cmdline = True
    preload_options = Command.preload_options + daemon_options('celerymon.pid')
    version = __version__

    def run(self, loglevel='ERROR', logfile=None, http_port=8989,
            http_address='', app=None, detach=False, pidfile=None,
            uid=None, gid=None, umask=None, working_directory=None, **kwargs):
        print('celerymon %s is starting.' % self.version)
        app = self.app
        workdir = working_directory

        # Setup logging
        if not isinstance(loglevel, int):
            loglevel = LOG_LEVELS[loglevel.upper()]

        # Dump configuration to screen so we have some basic information
        # when users sends e-mails.
        print(STARTUP_INFO_FMT % {
                'http_port': http_port,
                'http_address': http_address or 'localhost',
                'conninfo': app.broker_connection().as_uri(),
        })

        print('celerymon has started.')
        set_process_title('celerymon', info=strargv(sys.argv))

        def _run_monitor():
            create_pidlock(pidfile)
            app.log.setup_logging_subsystem(loglevel=loglevel,
                                            logfile=logfile)
            logger = app.log.get_default_logger(name='celery.mon')
            monitor = MonitorService(logger=logger,
                                     http_port=http_port,
                                     http_address=http_address)

            try:
                monitor.start()
            except Exception, exc:
                logger.error('celerymon raised exception %r',
                             exc, exc_info=True)
            except KeyboardInterrupt:
                pass

        if detach:
            with detached(logfile, pidfile, uid, gid, umask, workdir):
                _run_monitor()
        else:
            _run_monitor()

    def prepare_preload_options(self, options):
        workdir = options.get('working_directory')
        if workdir:
            os.chdir(workdir)

    def get_options(self):
        conf = self.app.conf
        return (
            Option('-l', '--loglevel',
                default=conf.CELERYMON_LOG_LEVEL,
                help='Choose between DEBUG/INFO/WARNING/ERROR/CRITICAL.'),
            Option('-P', '--port',
                type='int', dest='http_port', default=8989,
                help='Port the webserver should listen to.'),
            Option('-B', '--bind',
                dest='http_address', default='',
                help='Address webserver should listen to. Default (any).'),
            Option('-D', '--detach',
                action='store_true', help='Run as daemon.')
        )


try:
    # celery 3.x extension command
    from celery.bin.celery import Delegate

    class MonitorDelegate(Delegate):
        Command = MonitorCommand
except ImportError:
    class MonitorDelegate(object):  # noqa
        pass


def main():
    mon = MonitorCommand()
    mon.execute_from_commandline()


if __name__ == '__main__':
    main()
