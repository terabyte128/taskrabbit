# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0010_auto_20141221_1638'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name_plural': 'Statuses'},
        ),
        migrations.AlterField(
            model_name='note',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 26, 20, 30, 31, 872679)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='status',
            name='show_in_table',
            field=models.BooleanField(verbose_name='Show as active', default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateField(default=datetime.date(2014, 12, 26)),
            preserve_default=True,
        ),
    ]
