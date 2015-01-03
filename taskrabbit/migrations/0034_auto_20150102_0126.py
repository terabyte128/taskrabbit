# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0033_carrier_phonenumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phonenumber',
            name='carrier',
        ),
        migrations.DeleteModel(
            name='Carrier',
        ),
        migrations.RemoveField(
            model_name='phonenumber',
            name='user',
        ),
        migrations.DeleteModel(
            name='PhoneNumber',
        ),
    ]
