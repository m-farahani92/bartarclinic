# Generated by Django 5.1 on 2024-12-09 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0018_registerclass'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registerclass',
            old_name='ussername',
            new_name='username',
        ),
    ]
