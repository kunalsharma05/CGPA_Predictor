# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apogeeproj', '0003_lecture_hour_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('predicted_cg', models.IntegerField(null=True, blank=True)),
                ('week_attended', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Profile',
            },
        ),
    ]
