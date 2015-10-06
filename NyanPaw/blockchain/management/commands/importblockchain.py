﻿
import argparse
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.utils import IntegrityError

from blockchain.models import Block as dbBlock

from blocktools import Block

class Command(BaseCommand):
    help = 'import chain from from raw data files'
    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('path', type=argparse.FileType('rb'))

    def handle(self, *args, **options):
        f = options['path']

        i = 0
        with transaction.atomic():
            while True:
                b = Block(f)
                db = dbBlock.from_blocktools(b)
                try:
                    db.save()
                    print str(b)
                except IntegrityError as ie:
                    pass

                i += 1
                if i > 666:
                    break

        f.close()
