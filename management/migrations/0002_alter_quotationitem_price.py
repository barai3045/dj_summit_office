# Generated by Django 4.2.7 on 2024-02-16 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationitem',
            name='price',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=15),
        ),
    ]
