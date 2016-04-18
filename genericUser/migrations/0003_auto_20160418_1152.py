# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('genericUser', '0002_auto_20160418_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='message_datetime',
            field=models.DateField(default=datetime.datetime(2016, 4, 18, 11, 52, 15, 692704, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='reply',
            name='message_datetime',
            field=models.DateField(default=datetime.datetime(2016, 4, 18, 11, 52, 15, 693543, tzinfo=utc)),
        ),
    ]
