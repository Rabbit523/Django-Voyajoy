# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-26 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        #('bookingApp', '0012_remove_listing_owner_fees'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]