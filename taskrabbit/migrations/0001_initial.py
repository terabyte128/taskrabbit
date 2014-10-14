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
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500)),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2014, 10, 8, 22, 6, 31, 275070))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=256)),
                ('description', models.TextField(max_length=500, blank=True)),
                ('creation_date', models.DateField(default=datetime.date(2014, 10, 8))),
                ('last_worked_on', models.DateTimeField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, related_name='owner', null=True)),
                ('status', models.ForeignKey(related_name='status', to='taskrabbit.Status')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=128)),
                ('description', models.TextField(max_length=500, blank=True)),
                ('color', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
            field=models.ForeignKey(related_name='note_status', to='taskrabbit.Status'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='note',
            name='task',
            field=models.ForeignKey(related_name='task', to='taskrabbit.Task'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='note',
            name='user',
            field=models.ForeignKey(related_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
