# Generated by Django 4.1.7 on 2023-02-18 18:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(verbose_name='Широта')),
                ('longitude', models.FloatField(verbose_name='Долгота')),
                ('height', models.PositiveIntegerField(verbose_name='Высота')),
            ],
        ),
        migrations.CreateModel(
            name='SPRactivitiesTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('father_name', models.CharField(max_length=100, verbose_name='Отчество')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beauty_title', models.CharField(blank=True, default='', max_length=100, verbose_name='Название')),
                ('title', models.CharField(blank=True, default='', max_length=100, verbose_name='Название')),
                ('other_title', models.CharField(blank=True, default='', max_length=100, verbose_name='Название')),
                ('connect', models.CharField(blank=True, default='', max_length=100)),
                ('level_summer', models.CharField(blank=True, default='', max_length=10, verbose_name='Уровень сложности летом')),
                ('level_autumn', models.CharField(blank=True, default='', max_length=10, verbose_name='Уровень сложности осенью')),
                ('level_winter', models.CharField(blank=True, default='', max_length=10, verbose_name='Уровень сложности зимой')),
                ('level_spring', models.CharField(blank=True, default='', max_length=10, verbose_name='Уровень сложности весной')),
                ('date_added', models.DateTimeField(default=datetime.datetime.now)),
                ('status', models.CharField(choices=[('new', 'новая запись'), ('pending', 'в работе'), ('accepted', 'успешно создана'), ('rejected', 'запись не принята')], max_length=8)),
                ('coords', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coords', to='perevalapi.coordinates')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='perevalapi.users')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('image', models.ImageField(upload_to='photo/', verbose_name='Фото')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record', to='perevalapi.record')),
            ],
        ),
        migrations.CreateModel(
            name='Areas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='perevalapi.areas')),
            ],
        ),
    ]
