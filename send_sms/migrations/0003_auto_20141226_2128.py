# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('send_sms', '0002_auto_20141226_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonenumber',
            name='carrier',
            field=models.ForeignKey(null=True, to='send_sms.Carrier'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
