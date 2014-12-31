# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taskrabbit.models


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0027_auto_20141231_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountcreationid',
            name='email_address',
            field=models.TextField(null=True, max_length=128),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='accountcreationid',
            name='uuid',
            field=models.TextField(default=taskrabbit.models.get_random_id),
            preserve_default=True,
        ),
    ]
