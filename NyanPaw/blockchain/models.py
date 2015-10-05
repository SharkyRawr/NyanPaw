from django.db import models

import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)

# Create your models here.

class Block(models.Model):
    # Header
    Version = models.PositiveIntegerField()
    PreviousBlockHash = models.CharField(max_length=64)
    MerkleRoot = models.CharField(max_length=64)
    Time = models.PositiveIntegerField()
    Bits = models.PositiveIntegerField()
    Nonce = models.PositiveIntegerField()

    # Body
    Magic = models.CharField(max_length=8) # 4 bytes as hex
    Size = models.PositiveIntegerField()
    #Transactions = models.ForeignKey(Transaction, related_name='blocks')

    @staticmethod
    def from_blocktools(block):
        r = Block() # return val
        
        # Block Header
        h = block.blockHeader
        r.Version = h.version
        r.PreviousBlockHash = unicode(h.previousHash.encode('hex'))
        r.MerkleRoot = unicode(h.merkleHash.encode('hex'))
        r.Time = h.time
        r.Bits = h.bits
        r.Nonce = h.nonce

        # Block Body
        r.Magic = "%8x" % (block.magicNum)
        r.Size = block.blocksize

        r.save()

        # Transactions
        for btx in block.Txs:
            tx = Transaction(Version=btx.version, Locktime=btx.lockTime)
            tx.Block = r
            tx.save()

            for bin in btx.inputs:
                i = Input(PreviousTx=bin.prevhash.encode('hex'), TxOutId=bin.txOutId, ScriptSig=bin.scriptSig, Sequence=bin.seqNo)
                i.Transaction = tx
                i.save()

            for bout in btx.outputs:
                o = Output(Value=bout.value, PubKey=bout.pubkey)
                o.Transaction = tx
                o.save()

        # ToDo: Addresses http://bitcoin.stackexchange.com/a/19108

        return r

class Input(models.Model):
    PreviousTx = models.CharField(max_length=64)
    TxOutId = models.PositiveIntegerField()
    ScriptSig = models.BinaryField()
    Sequence = models.PositiveIntegerField()
    Transaction = models.ForeignKey('Transaction', related_name='Inputs')

class Output(models.Model):
    Value = models.PositiveIntegerField()
    PubKey = models.BinaryField()
    Transaction = models.ForeignKey('Transaction', related_name='Outputs')

class Transaction(models.Model):
    Version = models.PositiveIntegerField()
    #Inputs = models.PositiveIntegerField()
    #Outputs = models.PositiveIntegerField()
    Locktime = models.PositiveIntegerField()
    Block = models.ForeignKey(Block, related_name='Transactions')