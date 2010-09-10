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
from celery import conf
from celery import platform
from celery.log import emergency_error
from celery.utils import info

from celerymonitor.service import MonitorService

STARTUP_INFO_FMT = """
Configuration ->
    . broker -> %(conninfo)s
    . webserver -> http://%(http_address)s:%(http_port)s
""".strip()

OPTION_LIST = (
    optparse.make_option('-f', '--logfile', default=conf.CELERYMON_LOG_FILE,
            action="store", dest="logfile",
            help="Path to log file."),
    optparse.make_option('-l', '--loglevel',
            default=conf.CELERYMON_LOG_LEVEL,
            action="store", dest="loglevel",
            help="Choose between DEBUG/INFO/WARNING/ERROR/CRITICAL/FATAL."),
    optparse.make_option('-P', '--port',
            action="store", type="int", dest="http_port", default=8989,
            help="Port the webserver should listen to."),
    optparse.make_option('-A', '--address',
            action="store", type="string", dest="http_address",
            default="",
            help="Address the webserver should listen to. Default (any)."),
)


def run_monitor(loglevel=conf.CELERYMON_LOG_LEVEL,
        logfile=conf.CELERYMON_LOG_FILE, http_port=8989,
        http_address='', **kwargs):
    """Starts the celery monitor."""

    print("celerymon %s is starting." % celery.__version__)

    # Setup logging
    if not isinstance(loglevel, int):
        loglevel = conf.LOG_LEVELS[loglevel.upper()]

    # Dump configuration to screen so we have some basic information
    # when users sends e-mails.
    print(STARTUP_INFO_FMT % {
            "http_port": http_port,
            "http_address": http_address or "localhost",
            "conninfo": info.format_broker_info(),
    })

    from celery.log import setup_logger, redirect_stdouts_to_logger
    print("celerymon has started.")
    arg_start = "manage" in sys.argv[0] and 2 or 1
    platform.set_process_title("celerymon",
                               info=" ".join(sys.argv[arg_start:]))

    def _run_monitor():
        logger = setup_logger(loglevel, logfile)
        monitor = MonitorService(logger=logger,
                                 http_port=http_port,
                                 http_address=http_address)

        try:
            monitor.start()
        except Exception, e:
            emergency_error(logfile,
                    "celerymon raised exception %s: %s\n%s" % (
                            e.__class__, e, traceback.format_exc()))

    _run_monitor()


def parse_options(arguments):
    """Parse the available options to ``celerymon``."""
    parser = optparse.OptionParser(option_list=OPTION_LIST)
    options, values = parser.parse_args(arguments)
    return options


def main():
    options = parse_options(sys.argv[1:])
    run_monitor(**vars(options))

if __name__ == "__main__":
    main()
