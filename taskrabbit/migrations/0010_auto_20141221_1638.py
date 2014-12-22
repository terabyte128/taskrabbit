# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0009_auto_20141219_1737'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='due_date',
            new_name='end_date',
        ),
        migrations.RemoveField(
            model_name='task',
            name='creation_date',
        ),
        migrations.AddField(
            model_name='task',
            name='start_date',
            field=models.DateField(default=datetime.date(2014, 12, 21)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='note',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 21, 16, 38, 57, 900346)),
            preserve_default=True,
        ),
    ]
