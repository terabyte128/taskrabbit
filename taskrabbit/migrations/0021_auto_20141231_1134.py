# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0020_auto_20141228_2155'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountCreationID',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('uuid', models.TextField(default='c613b8d511b1404cb39adf3d5e697bbf')),
                ('expire_date', models.DateField(default=datetime.date(2015, 1, 1))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='note',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 31, 11, 34, 23, 521451)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateField(default=datetime.date(2014, 12, 31)),
            preserve_default=True,
        ),
    ]
