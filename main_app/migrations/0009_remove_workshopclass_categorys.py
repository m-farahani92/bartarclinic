# Generated by Django 5.1 on 2024-11-21 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_workshopclass_categorys_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshopclass',
            name='categoryS',
        ),
    ]