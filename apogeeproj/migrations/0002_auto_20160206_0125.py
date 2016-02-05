# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apogeeproj', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lec_type', models.CharField(max_length=20, choices=[(b'Tutorial', b'Tutorial'), (b'Lecture', b'Lecture'), (b'Practical', b'Practical')])),
                ('week_no', models.IntegerField(null=True, blank=True)),
                ('day_no', models.IntegerField(null=True, blank=True)),
                ('attendence', models.BooleanField(default=False)),
                ('evaluative', models.BooleanField(default=False)),
                ('max_marks', models.IntegerField(null=True, blank=True)),
                ('marks_obtained', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Lectures',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'subjects',
            },
        ),
        migrations.DeleteModel(
            name='Hi',
        ),
        migrations.AddField(
            model_name='lecture',
            name='subject',
            field=models.ForeignKey(to='apogeeproj.Subject'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
