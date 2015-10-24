# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('picture', models.ImageField(upload_to=b'')),
                ('description', models.TextField()),
                ('website', models.URLField()),
                ('location', models.CharField(default=b'Owatonna, MN', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=80)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('job_type', models.CharField(max_length=2, choices=[(b'FL', b'Full-time'), (b'PT', b'Part-time'), (b'CT', b'Contract'), (b'TY', b'Temporary'), (b'CN', b'Commission'), (b'IN', b'Internship')])),
                ('location', models.CharField(default=b'Owatonna, MN', max_length=30)),
                ('low_salary', models.IntegerField()),
                ('high_salary', models.IntegerField()),
                ('company', models.ForeignKey(to='board.Company')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('posts', models.ManyToManyField(to='board.Post')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='posts',
            field=models.ManyToManyField(to='board.Post'),
        ),
    ]
