# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_platform', '0003_auto_20150717_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='explanation',
            field=models.CharField(default=b'', max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='topic',
            field=models.ForeignKey(blank=True, to='test_platform.Topic', null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='description',
            field=models.CharField(default=b'', max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='description',
            field=models.CharField(default=b'', max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='topic_name',
            field=models.CharField(default=b'Other', max_length=100),
        ),
    ]
