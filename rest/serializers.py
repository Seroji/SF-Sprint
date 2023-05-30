from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from phonenumber_field.serializerfields import PhoneNumberField

from .models import (Coords,
                     Level,
                     Image,
                     PerevalAdded,
                     CustomUser,
                     PerevalImage)


class CoordsSerializer(serializers.ModelSerializer):
    height = serializers.IntegerField(required=True)
    longitude = serializers.FloatField(required=True)
    latitude = serializers.FloatField(required=True)

    class Meta:
        model = Coords
        fields = [
            'height',
            'longitude',
            'latitude',
        ]


class LevelSerializer(serializers.ModelSerializer):
    winter = serializers.CharField(required=False, default="", allow_blank=True)
    spring = serializers.CharField(required=False, default="", allow_blank=True)
    summer = serializers.CharField(required=False, default="", allow_blank=True)
    autumn = serializers.CharField(required=False, default="", allow_blank=True)

    class Meta:
        model = Level
        fields = [
            'winter',
            'spring',
            'summer',
            'autumn',
        ]


class ImageSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=64, required=True)
    image = serializers.ImageField(required=True)

    class Meta:
        model = Image
        fields = [
            'title',
            'image',
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    last_name = serializers.CharField(max_length=64, required=True)
    first_name = serializers.CharField(max_length=64, required=True)
    patronymic = serializers.CharField(max_length=64, required=True)
    phone = PhoneNumberField(region='RU', required=True)

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'last_name',
            'first_name',
            'patronymic',
            'phone'
        ]


class PerevalSerializer(serializers.ModelSerializer):
    coords = CoordsSerializer(many=False)
    level = LevelSerializer(many=False)
    images = ImageSerializer(many=True)
    user = CustomUserSerializer(many=False)
    connect = serializers.CharField(max_length=64, allow_blank=True)
    beauty_title = serializers.CharField(max_length=64, required=True)
    title = serializers.CharField(max_length=64, required=True)
    other_titles = serializers.CharField(max_length=64, required=True)
    add_time = serializers.DateTimeField(required=True)
    

    class Meta:
        model = PerevalAdded
        fields = [
            'beauty_title',
            'title',
            'other_titles',
            'connect',
            'add_time',
            'user',
            'coords',
            'level',
            'images',
        ]

    def create(self, validated_data):
        user = validated_data.pop('user')
        if not CustomUser.objects.filter(email=user.get('email')).exists():
            user_instance = CustomUser.objects.create(
                first_name=user.pop('first_name'),
                last_name=user.pop('last_name'),
                patronymic=user.pop('patronymic'),
                email=user.pop('email'),
                phone=user.pop('phone'),
            )
            user_instance.save()

        coords = validated_data.pop('coords')
        if not Coords.objects.filter(height=coords.get('height'), 
                                     longitude=coords.get('longitude'), 
                                     latitude=coords.get('latitude')).exists():
            coords_instance = Coords.objects.create(
                height=coords.pop('height'),
                longitude=coords.pop('longitude'),
                latitude=coords.pop('latitude'),
            )
            coords_instance.save()

        images = []
        for image in validated_data.pop('images'):
            image = Image.objects.create(
                title=image.pop('title'),
                image=image.pop('image')
            )
            image.save()
            images.append(image)
        
        level = validated_data.pop('level')
        level_instance = Level.objects.create(
            winter=level.pop('winter'),
            spring=level.pop('spring'),
            summer=level.pop('summer'),
            autumn=level.pop('autumn'),
        )
        level_instance.save()

        pereval = PerevalAdded.objects.create(
            beauty_title = validated_data.pop('beauty_title'),
            title=validated_data.pop('title'),
            other_titles=validated_data.pop('other_titles'),
            user_id=user_instance.id,
            coords_id=coords_instance.id,
            level_id=level_instance.id,
        )
        pereval.save()

        for image in images:
            PerevalImage.objects.create(pereval_id=pereval.id, image_id=image.id)
        return pereval
