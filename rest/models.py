from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class CustomUser(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    phone = models.IntegerField(null=False, default=9999999999)

    @receiver(signal=post_save, sender=User)
    def create_user_author(sender, instance, created, **kwargs):
        if created:
            obj = CustomUser.objects.create(user=instance)
            obj.save()


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
    add_time = models.DateTimeField(auto_now_add=True)
    connect = models.ForeignKey('Connect',
                                default=1,
                                on_delete=models.CASCADE)
    status = models.ForeignKey('Status',
                               default=1,
                               on_delete=models.CASCADE)
    coords = models.ForeignKey('Coords',
                               on_delete=models.CASCADE)
    level = models.ForeignKey('Level',
                              on_delete=models.CASCADE)
    images = models.ManyToManyField("Image",
                                    through='PerevalImage')
    

class Connect(models.Model):
    title = models.CharField(max_length=64)


class Status(models.Model):
    title = models.CharField(max_length=64)
    
    
class Coords(models.Model):
    height = models.IntegerField(null=False)
    logitude = models.FloatField(null=False)
    latitude = models.FloatField(null=False)


class Level(models.Model):
    winter = models.CharField(max_length=4)
    spring = models.CharField(max_length=4)
    summer = models.CharField(max_length=4)
    autumn = models.CharField(max_length=4)

class Image(models.Model):
    title = models.CharField(max_length=64)
    image = models.BinaryField(editable=True, null=False)


class PerevalImage(models.Model):
    pereval = models.ForeignKey(PerevalAdded,
                                on_delete=models.CASCADE)
    image = models.ForeignKey(Image,
                              on_delete=models.CASCADE)
