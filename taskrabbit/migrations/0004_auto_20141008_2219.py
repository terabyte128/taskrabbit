# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0003_auto_20141008_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='show_in_table',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='note',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 8, 22, 19, 33, 27154)),
        ),
    ]
