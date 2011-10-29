from __future__ import absolute_import

from djcelery.app import app
from djcelery.management.base import CeleryCommand

from celerymon.bin.celerymon import MonitorCommand

monitor = MonitorCommand(app=app)


class Command(CeleryCommand):
    """Run the celery monitor."""
    option_list = CeleryCommand.option_list + monitor.get_options()
    help = 'Run the celery monitor'

    def handle(self, *args, **options):
        """Handle the management command."""
        monitor.run(**options)
