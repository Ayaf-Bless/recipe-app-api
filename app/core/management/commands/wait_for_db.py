import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause exec until DB is ready"""

    def handle(self, *args, **options):
        self.stdout.write("Waiting for Database")
        db_con = None
        while not db_con:
            try:
                db_con = connections["default"]
            except OperationalError:
                self.stdout.write("Database unvailable, waiting 1 sec...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
