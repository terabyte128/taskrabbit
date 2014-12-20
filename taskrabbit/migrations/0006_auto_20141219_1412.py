# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0005_auto_20141219_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 19, 14, 12, 1, 192049)),
            preserve_default=True,
        ),
    ]
