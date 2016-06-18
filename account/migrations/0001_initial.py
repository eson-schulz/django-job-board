# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('picture', models.ImageField(upload_to=b'companies/', blank=True)),
                ('description', models.TextField(blank=True)),
                ('website', models.URLField(blank=True)),
                ('location', models.CharField(default=b'Owatonna, MN', max_length=30, blank=True)),
                ('stripe_id', models.CharField(max_length=50, null=True, blank=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('stripe_id', models.CharField(max_length=20)),
                ('max_posts', models.PositiveSmallIntegerField()),
                ('max_upgraded_posts', models.PositiveSmallIntegerField()),
                ('company_image', models.BooleanField(default=False)),
                ('social_links', models.BooleanField(default=False)),
                ('social_post', models.BooleanField(default=False)),
                ('email_post', models.BooleanField(default=False)),
                ('visible', models.BooleanField(default=True)),
                ('cost', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='plan',
            field=models.ForeignKey(to='account.Plan'),
        ),
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
