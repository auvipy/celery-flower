#!/usr/bin/env python
"""celerymon

.. program:: celerymon

.. cmdoption:: -P, --port

    Port the webserver should listen to. Default: ``8989``.

.. cmdoption:: -A, --address

    Address the webserver should listen to. Default (any).

.. cmdoption:: -f, --logfile

    Path to log file. If no logfile is specified, ``stderr`` is used.

.. cmdoption:: -l, --loglevel

    Logging level, choose between ``DEBUG``, ``INFO``, ``WARNING``,
    ``ERROR``, ``CRITICAL``, or ``FATAL``.

"""
import os
import sys
import traceback
import optparse

import celery
from celery import platforms
from celery.app import app_or_default
from celery.bin.base import Command, Option
from celery.utils import LOG_LEVELS

from celerymonitor.service import MonitorService

STARTUP_INFO_FMT = """
Configuration ->
    . broker -> %(conninfo)s
    . webserver -> http://%(http_address)s:%(http_port)s
""".strip()

OPTION_LIST = (
)


class MonitorCommand(Command):
    namespace = "celerymon"
    enable_config_from_cmdline = True

    def run(self, loglevel="ERROR", logfile=None, http_port=8989,
            http_address='', app=None, **kwargs):
        print("celerymon %s is starting." % celery.__version__)
        app = self.app

        # Setup logging
        if not isinstance(loglevel, int):
            loglevel = LOG_LEVELS[loglevel.upper()]

        # Dump configuration to screen so we have some basic information
        # when users sends e-mails.
        print(STARTUP_INFO_FMT % {
                "http_port": http_port,
                "http_address": http_address or "localhost",
                "conninfo": app.broker_connection().as_uri(),
        })

        print("celerymon has started.")
        arg_start = "manage" in sys.argv[0] and 2 or 1
        platforms.set_process_title("celerymon",
                                    info=" ".join(sys.argv[arg_start:]))

        def _run_monitor():
            app.log.setup_logging_subsystem(loglevel=loglevel,
                                            logfile=logfile)
            logger = app.log.get_default_logger(name="celery.mon")
            monitor = MonitorService(logger=logger,
                                     http_port=http_port,
                                     http_address=http_address)

            try:
                monitor.start()
            except Exception, exc:
                logger.error("celerymon raised exception %r\n%s" % (
                                exc, traceback.format_exc()))

        _run_monitor()

    def get_options(self):
        conf = self.app.conf
        return (
            Option('-f', '--logfile', default=conf.CELERYMON_LOG_FILE,
                    action="store", dest="logfile",
                    help="Path to log file."),
            Option('-l', '--loglevel',
                    default=conf.CELERYMON_LOG_LEVEL,
                    action="store", dest="loglevel",
                    help="Choose between DEBUG/INFO/WARNING/ERROR/CRITICAL."),
            Option('-P', '--port',
                action="store", type="int", dest="http_port", default=8989,
                help="Port the webserver should listen to."),
        Option('-A', '--address',
                action="store", type="string", dest="http_address",
                default="",
                help="Address webserver should listen to. Default (any)."),
    )


def main():
    mon = MonitorCommand()
    mon.execute_from_commandline()


if __name__ == "__main__":
    main()
