# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0004_auto_20141008_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='automatic_note',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='note',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 9, 13, 17, 20, 613489)),
        ),
        migrations.AlterField(
            model_name='task',
            name='creation_date',
            field=models.DateField(default=datetime.date(2014, 10, 9)),
        ),
    ]
