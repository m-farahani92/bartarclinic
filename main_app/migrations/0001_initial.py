# Generated by Django 5.1 on 2024-11-18 10:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='categoryClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='categorywsClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='contactClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('title', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='staticcontentClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=10)),
                ('txt', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='serviceClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.categoryclass')),
            ],
        ),
        migrations.CreateModel(
            name='workshopClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('startw', models.CharField(max_length=30)),
                ('price', models.IntegerField()),
                ('numbsession', models.CharField(max_length=50)),
                ('numbparticipants', models.CharField(max_length=30)),
                ('img', models.ImageField(null=True, upload_to='photo')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='w', to='main_app.categorywsclass')),
            ],
        ),
    ]
