from django.db import models
from django.db.models.signals import pre_save

from blockchain.util import calculate_difficulty, hash_to_address
from blockchain.util.base58 import b58encode, b58decode

import binascii

# Create your models here.

class Block(models.Model):
    # Header
    Version = models.PositiveIntegerField()
    Hash = models.CharField(max_length=64, unique=True)
    PreviousBlockHash = models.CharField(max_length=64)
    MerkleRoot = models.CharField(max_length=64, unique=True)
    Time = models.PositiveIntegerField()
    Bits = models.PositiveIntegerField()
    Difficulty = models.FloatField()
    Nonce = models.PositiveIntegerField()

    # Body
    Magic = models.CharField(max_length=8) # 4 bytes as hex
    Size = models.PositiveIntegerField()
    #Transactions = models.ForeignKey(Transaction, related_name='blocks')

    @staticmethod
    def from_blocktools(block):
        try:
            r = Block.objects.get(Hash=block.blockHeader.hash())
            return r
        except Block.DoesNotExist:
            r = Block()

        # Block Header
        h = block.blockHeader
        r.Version = h.version
        r.PreviousBlockHash = str(binascii.hexlify(h.previousHash))
        r.MerkleRoot = str(binascii.hexlify(h.merkleHash))
        r.Time = h.time
        r.Bits = h.bits
        r.Difficulty = calculate_difficulty(r.Bits)
        r.Nonce = h.nonce

        # Block Body
        r.Hash = h.hash()
        r.Magic = "%8x" % (block.magicNum)
        r.Size = block.blocksize

        r.save()

        # Transactions
        for btx in block.Txs:
            tx = Transaction(Version=btx.version, Locktime=btx.lockTime)
            tx.Block = r
            tx.save()

            for bin in btx.inputs:
                i = Input(PreviousTx=binascii.hexlify(bin.prevhash), TxOutId=bin.txOutId, ScriptSig=bin.scriptSig, Sequence=bin.seqNo)
                i.Transaction = tx
                i.save()

            for bout in btx.outputs:
                o = Output(Value=bout.value, PubKey=bout.pubkey)
                o.Transaction = tx
                o.save()

        # ToDo: Addresses http://bitcoin.stackexchange.com/a/19108

        return r

class Transaction(models.Model):
    Version = models.PositiveIntegerField()
    Locktime = models.PositiveIntegerField()
    Block = models.ForeignKey(Block, related_name='Transactions')

class Input(models.Model):
    PreviousTx = models.CharField(max_length=64)
    TxOutId = models.PositiveIntegerField()
    ScriptSig = models.BinaryField()
    Sequence = models.PositiveIntegerField()
    Transaction = models.ForeignKey(Transaction, related_name='Inputs')

class Output(models.Model):
    Value = models.PositiveIntegerField()
    PubKey = models.BinaryField()
    Transaction = models.ForeignKey(Transaction, related_name='Outputs')
    Address = models.CharField(max_length=128)

    @staticmethod
    def pre_save(sender, instance, **kwargs):
        pubkey = instance.PubKey
        # OP_DUP OP_HASH160 <pubKeyHash>
        if pubkey[0] == 0x76 and pubkey[1] == 0xa9:
            numBytes = pubkey[2]
            h = bytes(pubkey[3:3+numBytes])
            version = bytes(b'-')
            instance.Address = hash_to_address(version, h)


pre_save.connect(Output.pre_save, Output, dispatch_uid="blockchain.models.Output")
