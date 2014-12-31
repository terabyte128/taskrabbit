# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taskrabbit.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0023_auto_20141231_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountcreationid',
            name='expire_date',
            field=models.DateTimeField(default=taskrabbit.models.add_1_day),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='accountcreationid',
            name='uuid',
            field=models.TextField(default='347eb24c59034486a128d2be4bcedef4'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='note',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateField(default=datetime.date.today),
            preserve_default=True,
        ),
    ]
