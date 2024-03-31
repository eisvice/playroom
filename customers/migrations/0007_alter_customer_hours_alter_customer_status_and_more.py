# Generated by Django 5.0.1 on 2024-03-29 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_playgrounddetail_rate_alter_customer_hours_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='hours',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
        migrations.AlterField(
            model_name='customer',
            name='status',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='playgrounddetail',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='playgrounddetail',
            name='rate',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='playgrounddetail',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
