# Generated by Django 5.0.1 on 2024-04-03 10:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0011_remove_playgrounddetail_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_permission_given',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playgrounddetail',
            name='date',
            field=models.DateField(default=datetime.date(2024, 4, 3)),
        ),
    ]
