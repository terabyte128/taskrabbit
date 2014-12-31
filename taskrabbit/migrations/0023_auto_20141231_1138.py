# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0022_auto_20141231_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountcreationid',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='accountcreationid',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 1, 11, 38, 18, 953449)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='accountcreationid',
            name='uuid',
            field=models.TextField(default='bd64e6d70b454b869c5e123767b496d0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='note',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 31, 11, 38, 18, 950166)),
            preserve_default=True,
        ),
    ]
