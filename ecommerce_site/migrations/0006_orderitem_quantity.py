# Generated by Django 3.1.5 on 2021-01-16 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_site', '0005_item_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
