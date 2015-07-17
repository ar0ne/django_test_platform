# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_platform', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='description',
            field=models.CharField(default=b'', max_length=500),
        ),
        migrations.AddField(
            model_name='topic',
            name='desciption',
            field=models.CharField(default=b'', max_length=500),
        ),
        migrations.AlterField(
            model_name='question',
            name='explanation',
            field=models.CharField(default=b'', max_length=300),
        ),
    ]
