# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taskrabbit', '0005_auto_20141009_1317'),
    ]

    operations = [
        migrations.CreateModel(
            name='NfcCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('card_name', models.CharField(max_length=64)),
                ('serial_number', models.CharField(max_length=64)),
                ('secret_key', models.CharField(max_length=64)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry_time', models.DateTimeField()),
                ('exit_time', models.DateTimeField(null=True)),
                ('valid', models.BooleanField(default=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='note',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 12, 16, 11, 33, 791629)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='creation_date',
            field=models.DateField(default=datetime.date(2014, 12, 12)),
            preserve_default=True,
        ),
    ]
