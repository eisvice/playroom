# Generated by Django 5.0.1 on 2024-04-02 15:42

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0009_alter_customer_start_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playground',
            name='user',
        ),
        migrations.AddField(
            model_name='user',
            name='playground',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='customers.playground'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playground',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='playgrounddetail',
            name='date',
            field=models.DateField(default=datetime.date(2024, 4, 2)),
        ),
    ]