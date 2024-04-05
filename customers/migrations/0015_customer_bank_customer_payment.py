# Generated by Django 5.0.1 on 2024-04-04 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0014_alter_playgrounddetail_date_alter_user_is_owner_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='bank',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='payment',
            field=models.CharField(default='cash', max_length=10),
        ),
    ]
