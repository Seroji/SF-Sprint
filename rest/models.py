from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=64, 
                                  default='Имя')
    last_name = models.CharField(max_length=64, 
                                 default='Фамилия')
    patronymic = models.CharField(max_length=64, 
                                  default='Отчество')
    phone = PhoneNumberField(region='RU', null=False)
    email = models.EmailField(max_length=64, 
                              unique=True, 
                              default='example@mail.ru', 
                              null=False)
    
    USERNAME_FIELD = 'email'

    
class PerevalAdded(models.Model):
    user = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE)
    beauty_title = models.CharField(max_length=64, 
                                    default='пер.')
    title = models.CharField(max_length=64, 
                             null=False, 
                             default='Название')
    other_titles = models.CharField(max_length=128, 
                                    null=False, 
                                    default='Другие названия')
    add_time = models.DateTimeField()
    connect = models.CharField(null=True)
    status = models.ForeignKey('Status',
                               default=1,
                               on_delete=models.CASCADE)
    coords = models.ForeignKey('Coords',
                               on_delete=models.CASCADE)
    level = models.ForeignKey('Level',
                              on_delete=models.CASCADE)
    images = models.ManyToManyField("Image",
                                    through='PerevalImage')


class Status(models.Model):
    title = models.CharField(max_length=64)
    
    
class Coords(models.Model):
    height = models.IntegerField(null=False)
    longitude = models.FloatField(null=False)
    latitude = models.FloatField(null=False)


class Level(models.Model):
    winter = models.CharField(max_length=2, default="", blank=False)
    spring = models.CharField(max_length=2, default="", blank=False)
    summer = models.CharField(max_length=2, default="", blank=False)
    autumn = models.CharField(max_length=2, default="", blank=False)


class Image(models.Model):
    title = models.CharField(max_length=64)
    image = models.ImageField(null=False)


class PerevalImage(models.Model):
    pereval = models.ForeignKey(PerevalAdded,
                                on_delete=models.CASCADE)
    image = models.ForeignKey(Image,
                              on_delete=models.CASCADE)
