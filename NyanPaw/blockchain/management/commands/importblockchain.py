
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
        parser.add_argument('pathToBlockchain', type=argparse.FileType('rb'))
        parser.add_argument('--truncate', action='store_true')
        parser.add_argument('--resume', type=int)

    def handle(self, *args, **options):
        f = options['pathToBlockchain']

        if options['resume'] is not None:
            f.seek(options['resume'], 0)

        if options['truncate'] is True:
            print ("Truncating database ...")
            dbBlock.objects.all().delete()

        print ("Parsing blockchain ...")
        i = 0
        with transaction.atomic():
            while True:
                b = Block(f)
                db = dbBlock.from_blocktools(b)
                try:
                    db.save()
                    #print (str(b))
                    print ("Position:", f.tell())
                except IntegrityError as ie:
                    pass

                i += 1
                if i >= 1000:
                    break

        f.close()
