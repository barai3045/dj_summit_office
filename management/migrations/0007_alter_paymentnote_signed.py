# Generated by Django 4.2.7 on 2024-04-03 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_paymentnote_signed_alter_paymentnoteinvoice_note_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentnote',
            name='signed',
            field=models.BooleanField(default=False),
        ),
    ]
