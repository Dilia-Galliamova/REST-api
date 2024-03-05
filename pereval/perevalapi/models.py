from datetime import datetime

from django.conf import settings
from django.db import models


STATUS_TYPE = [
    ('new', 'новая запись'),
    ('pending', 'в работе'),
    ('accepted', 'успешно создана'),
    ('rejected', 'запись не принята')
]


class Users(models.Model):
    email = models.CharField(max_length=150, unique=True)
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    father_name = models.CharField('Отчество', max_length=100)
    phone = models.CharField('Телефон', max_length=20)


class Coordinates(models.Model):
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    height = models.PositiveIntegerField('Высота')


class Record(models.Model):
    beauty_title = models.CharField('Название 1', blank=True, default='', max_length=100)
    title = models.CharField('Название 2', blank=True, default='', max_length=100)
    other_title = models.CharField('Название 3', blank=True, default='', max_length=100)
    connect = models.CharField(blank=True, default='', max_length=100)
    level_summer = models.CharField('Уровень сложности летом', blank=True, default='', max_length=10)
    level_autumn = models.CharField('Уровень сложности осенью', blank=True, default='', max_length=10)
    level_winter = models.CharField('Уровень сложности зимой', blank=True, default='', max_length=10)
    level_spring = models.CharField('Уровень сложности весной', blank=True, default='', max_length=10)
    date_added = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=8, choices=STATUS_TYPE)

    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user')
    coords = models.ForeignKey(Coordinates, on_delete=models.CASCADE, related_name='coords')


class Images(models.Model):
    title = models.CharField('Название', max_length=150)
    image = models.ImageField('Фото', upload_to='photo/', blank=False, null=False)
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='image')


class SPRactivitiesTypes(models.Model):
    title = models.CharField('Название', max_length=150)


class Areas(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField('Название', max_length=150)
