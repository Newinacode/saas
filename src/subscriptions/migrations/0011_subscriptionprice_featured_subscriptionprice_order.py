# Generated by Django 5.0.7 on 2024-07-31 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0010_alter_subscriptionprice_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionprice',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subscriptionprice',
            name='order',
            field=models.IntegerField(default=-1),
        ),
    ]
