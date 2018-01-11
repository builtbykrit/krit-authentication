# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SignupCode',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('code', models.CharField(unique=True, max_length=64, verbose_name='code')),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('sent', models.DateTimeField(null=True, verbose_name='sent', blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now,
                                                 editable=False, verbose_name='created')),
                ('inviter', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL,
                                              null=True, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'signup code',
                'verbose_name_plural': 'signup codes',
            },
        ),
        migrations.CreateModel(
            name='SignupCodeResult',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('signup_code', models.ForeignKey(to='registration.SignupCode', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
    ]
