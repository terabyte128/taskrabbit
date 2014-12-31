# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0029_remove_nfccard_secret_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nfccard',
            name='user',
        ),
        migrations.DeleteModel(
            name='NfcCard',
        ),
    ]
