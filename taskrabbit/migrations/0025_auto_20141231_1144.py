# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskrabbit', '0024_auto_20141231_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountcreationid',
            name='uuid',
            field=models.TextField(default='d834b71385254981bba400bfca86ccec'),
            preserve_default=True,
        ),
    ]
