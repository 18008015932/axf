# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-08 03:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0002_auto_20180508_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodelticket',
            name='out_time',
            field=models.DateField(),
        ),
    ]
