# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('send_sms', '0003_auto_20141226_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonenumber',
            name='phone_number',
            field=models.IntegerField(null=True, max_length=10),
            preserve_default=True,
        ),
    ]
