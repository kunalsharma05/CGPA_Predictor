# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apogeeproj', '0002_auto_20160206_0125'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='hour_no',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
