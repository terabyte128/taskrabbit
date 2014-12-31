# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0028_auto_20141231_1203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nfccard',
            name='secret_key',
        ),
    ]
