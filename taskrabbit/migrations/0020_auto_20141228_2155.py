# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0019_auto_20141226_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 28, 21, 55, 3, 823373)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateField(default=datetime.date(2014, 12, 28)),
            preserve_default=True,
        ),
    ]
