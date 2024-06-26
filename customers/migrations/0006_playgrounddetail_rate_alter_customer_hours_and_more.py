# Generated by Django 5.0.1 on 2024-03-29 15:26

import datetime
import django.db.models.functions.datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_customer_playground_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='playgrounddetail',
            name='rate',
            field=models.DecimalField(decimal_places=2, default=350.0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='customer',
            name='hours',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='customer',
            name='start_time',
            field=models.DateTimeField(db_default=django.db.models.functions.datetime.Now()),
        ),
        migrations.AlterField(
            model_name='customer',
            name='status',
            field=models.CharField(default='active', max_length=20),
        ),
        migrations.AlterField(
            model_name='playgrounddetail',
            name='date',
            field=models.DateField(default=datetime.date(2024, 3, 29)),
        ),
    ]
