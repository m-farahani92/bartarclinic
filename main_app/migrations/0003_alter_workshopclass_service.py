# Generated by Django 5.1 on 2025-01-04 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_workshopclass_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopclass',
            name='service',
            field=models.ForeignKey(limit_choices_to={'category__title': 'برگزاری کارگاه'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.serviceclass'),
        ),
    ]
