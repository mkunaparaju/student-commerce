# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_auto_20151219_0845'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.DeleteModel(
            name='TagBook',
        ),
    ]
