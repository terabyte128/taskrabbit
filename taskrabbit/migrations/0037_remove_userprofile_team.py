# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0036_auto_20150104_1130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='team',
        ),
    ]
