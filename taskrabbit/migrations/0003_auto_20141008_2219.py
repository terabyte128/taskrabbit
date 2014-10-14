# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0002_auto_20141008_2218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='show_in_table',
        ),
        migrations.AlterField(
            model_name='note',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 8, 22, 19, 14, 183791)),
        ),
    ]
