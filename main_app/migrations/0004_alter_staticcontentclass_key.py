# Generated by Django 5.1 on 2024-11-20 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_staticphotoclass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticcontentclass',
            name='key',
            field=models.CharField(max_length=15),
        ),
    ]