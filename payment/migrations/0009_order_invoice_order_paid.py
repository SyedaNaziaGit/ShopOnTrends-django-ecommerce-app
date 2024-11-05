# Generated by Django 5.1.2 on 2024-11-04 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0008_order_date_shipped'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='invoice',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
