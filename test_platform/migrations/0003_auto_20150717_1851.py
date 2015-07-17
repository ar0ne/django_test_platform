# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_platform', '0002_auto_20150717_1708'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='desciption',
            new_name='description',
        ),
    ]
