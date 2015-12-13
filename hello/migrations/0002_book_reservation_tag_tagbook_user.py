# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.AutoField(serialize=False, primary_key=True, db_column='BOOK_ID')),
                ('avail_start', models.TimeField(db_column='AVAIL_START')),
                ('avail_end', models.TimeField(db_column='AVAIL_END')),
                ('name', models.CharField(max_length=50, db_column='NAME')),
            ],
            options={
                'db_table': 'book',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('reserved_id', models.AutoField(serialize=False, primary_key=True, db_column='RESERVED_ID')),
                ('reserved_start', models.TimeField(db_column='RESERVED_START')),
                ('reserved_end', models.TimeField(db_column='RESERVED_END')),
                ('name_book', models.CharField(max_length=50, db_column='NAME_BOOK')),
            ],
            options={
                'db_table': 'reservation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tag_id', models.AutoField(serialize=False, primary_key=True, db_column='TAG_ID')),
                ('tag_name', models.CharField(max_length=45, db_column='TAG_NAME')),
            ],
            options={
                'db_table': 'tag',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TagBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'tag_book',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(serialize=False, primary_key=True, db_column='USER_ID')),
                ('email_id', models.CharField(max_length=45, db_column='EMAIL_ID')),
                ('pswd', models.CharField(max_length=45, db_column='PSWD')),
                ('nickname', models.CharField(max_length=45, null=True, db_column='NICKNAME', blank=True)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
    ]
