# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255, null=True, blank=True)),
                ('image', models.CharField(max_length=255, null=True, blank=True)),
                ('price', models.FloatField(default=0, null=True)),
            ],
        ),
    ]
