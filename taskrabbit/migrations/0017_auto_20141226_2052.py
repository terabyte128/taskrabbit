# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0016_auto_20141226_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 26, 20, 52, 50, 953229)),
            preserve_default=True,
        ),
    ]
