# Generated by Django 5.0.1 on 2024-04-27 20:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0017_alter_playgrounddetail_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playgrounddetail',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
