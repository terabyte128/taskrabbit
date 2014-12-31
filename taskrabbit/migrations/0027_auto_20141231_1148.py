# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taskrabbit.models


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0026_auto_20141231_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountcreationid',
            name='uuid',
            field=models.TextField(default=taskrabbit.models.get_random_id, auto_created=True),
            preserve_default=True,
        ),
    ]
