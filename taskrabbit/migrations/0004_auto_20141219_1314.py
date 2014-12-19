# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0003_auto_20141214_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 19, 13, 14, 47, 643134)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='creation_date',
            field=models.DateField(default=datetime.date(2014, 12, 19)),
            preserve_default=True,
        ),
    ]
