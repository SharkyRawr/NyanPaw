
import argparse
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.utils import IntegrityError

from tqdm import tqdm

from blockchain.models import Block as dbBlock
from config.models import ConfigItem

from blocktools import Block


class Command(BaseCommand):
    help = 'import chain from from raw data files'
    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('pathToBlockchain', type=argparse.FileType('rb'))
        parser.add_argument('--truncate', action='store_true')

    def handle(self, *args, **options):
        f = options['pathToBlockchain']

        f.seek(0, 2)    # seek to end
        chainLen = f.tell()
        f.seek(0, 0)    # and back to beginning

        lastBlockIndex = 0
        lastBlockIndexKV, created = ConfigItem.objects.get_or_create(
            Key='lastBlockIndex')

        lastBlockPos, created = ConfigItem.objects.get_or_create(
            Key='lastBlockPos')
        if not created and options['truncate'] is False:
            print("Resuming blockchain from", lastBlockPos.Value or '0')
            f.seek(int(lastBlockPos.Value or '0'), 0)
            lastBlockIndex = int(lastBlockIndexKV.Value or '0')

        if options['truncate'] is True:
            print("Truncating database ...")
            dbBlock.objects.all().delete()

        print("Parsing blockchain ...")
        i = 0
        cont = True
        with tqdm(total=chainLen, initial=int(lastBlockPos.Value)) as pbar:

            while cont is True:
                blockBuffer = []

                try:

                    for i in range(250):
                        b = Block(f)
                        blockBuffer.append(b)

                except (KeyboardInterrupt, SystemExit):
                    cont = False


                with transaction.atomic():
                    for b in blockBuffer:
                        try:
                            db = dbBlock.from_blocktools(b, lastBlockIndex)
                            db.save()
                            #print (str(b))

                            chainPos = f.tell()
                            pbar.update(chainPos - int(lastBlockPos.Value))
                            #print ("update", chainPos - int(lastBlockPos.Value))

                            lastBlockPos.Value = str(chainPos)
                            lastBlockPos.save()
                            lastBlockIndex += 1
                            lastBlockIndexKV.Value = str(lastBlockIndex)
                            lastBlockIndexKV.save()
                        except IntegrityError as ie:
                            print("Error:", ie)
                            raise
                        except KeyboardInterrupt:
                            cont = False

                #i += 1
                #if i >= 5000:
                #    cont = False
        f.close()
