# Generated by Django 5.1 on 2025-02-01 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_remove_reservationclass_payment_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleclass',
            name='is_available',
            field=models.BooleanField(default=True, verbose_name='آیا وقت آزاد است؟'),
        ),
    ]
