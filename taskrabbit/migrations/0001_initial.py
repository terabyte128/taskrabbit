# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NfcCard',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
            name='Note',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('content', models.TextField(max_length=500)),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2014, 12, 12, 17, 19, 59, 542605))),
                ('automatic_note', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.TextField(max_length=100)),
                ('show_in_table', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.TextField(max_length=256)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('creation_date', models.DateField(default=datetime.date(2014, 12, 12))),
                ('last_worked_on', models.DateTimeField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, related_name='owner')),
                ('status', models.ForeignKey(to='taskrabbit.Status', related_name='status')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.TextField(max_length=128)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('color', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeLog',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('entry_time', models.DateTimeField()),
                ('exit_time', models.DateTimeField(null=True)),
                ('valid', models.BooleanField(default=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('team', models.ForeignKey(to='taskrabbit.Team')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='task',
            name='team',
            field=models.ForeignKey(to='taskrabbit.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='note',
            name='status',
            field=models.ForeignKey(to='taskrabbit.Status', related_name='note_status'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='note',
            name='task',
            field=models.ForeignKey(to='taskrabbit.Task', related_name='task'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='note',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user'),
            preserve_default=True,
        ),
    ]
