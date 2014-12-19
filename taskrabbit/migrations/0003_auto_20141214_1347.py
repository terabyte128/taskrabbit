# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0002_auto_20141212_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='timelog',
            name='time_length',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='note',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 14, 13, 47, 3, 54907)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='creation_date',
            field=models.DateField(default=datetime.date(2014, 12, 14)),
            preserve_default=True,
        ),
    ]
