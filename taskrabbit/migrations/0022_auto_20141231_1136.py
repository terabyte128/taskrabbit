# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0021_auto_20141231_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountcreationid',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 1, 11, 36, 19, 738763)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='accountcreationid',
            name='uuid',
            field=models.TextField(default='6468c2b578524dd3b5ad3a1a6e4c89db'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='note',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 31, 11, 36, 19, 733666)),
            preserve_default=True,
        ),
    ]
