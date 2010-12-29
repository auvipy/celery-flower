"""

Start the celery clock service from the Django management command.

"""
from djcelery.app import app
from djcelery.management.base import CeleryCommand

from celerymonitor.bin.celerymond import MonitorCommand

monitor = MonitorCommand(app=app)


class Command(CeleryCommand):
    """Run the celery monitor."""
    option_list = CeleryCommand.option_list + monitor.get_options()
    help = 'Run the celery monitor'

    def handle(self, *args, **options):
        """Handle the management command."""
        monitor.run(**options)
