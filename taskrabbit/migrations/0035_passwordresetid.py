# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taskrabbit.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taskrabbit', '0034_auto_20150102_0126'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordResetID',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('uuid', models.TextField(default=taskrabbit.models.get_random_id)),
                ('expire_date', models.DateTimeField(default=taskrabbit.models.add_1_day)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
