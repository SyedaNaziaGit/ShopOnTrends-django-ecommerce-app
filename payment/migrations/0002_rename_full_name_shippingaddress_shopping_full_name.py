# Generated by Django 5.1.2 on 2024-10-25 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='full_name',
            new_name='shopping_full_name',
        ),
    ]
