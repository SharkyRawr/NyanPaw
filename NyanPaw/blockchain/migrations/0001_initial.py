# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Version', models.PositiveIntegerField()),
                ('PreviousBlockHash', models.CharField(max_length=64)),
                ('MerkleRoot', models.CharField(max_length=64)),
                ('Time', models.PositiveIntegerField()),
                ('Bits', models.PositiveIntegerField()),
                ('Nonce', models.PositiveIntegerField()),
                ('Magic', models.CharField(max_length=8)),
                ('Size', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Input',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('PreviousTx', models.CharField(max_length=64)),
                ('TxOutId', models.PositiveIntegerField()),
                ('ScriptSig', models.BinaryField()),
                ('Sequence', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Value', models.PositiveIntegerField()),
                ('PubKey', models.BinaryField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Version', models.PositiveIntegerField()),
                ('Locktime', models.PositiveIntegerField()),
                ('Block', models.ForeignKey(related_name='Transactions', to='blockchain.Block')),
            ],
        ),
        migrations.AddField(
            model_name='output',
            name='Transaction',
            field=models.ForeignKey(related_name='Outputs', to='blockchain.Transaction'),
        ),
        migrations.AddField(
            model_name='input',
            name='Transaction',
            field=models.ForeignKey(related_name='Inputs', to='blockchain.Transaction'),
        ),
    ]
