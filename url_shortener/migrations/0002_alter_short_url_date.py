# Generated by Django 4.2 on 2023-04-12 04:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_shortener', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='short_url',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 4, 12, 4, 56, 23, 508879, tzinfo=datetime.timezone.utc)),
        ),
    ]
