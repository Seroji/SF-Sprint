from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import (Coords,
                     Level,
                     Image,
                     PerevalAdded,
                     CustomUser,
                     PerevalImage)


class CoordsSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Image
        fields = [
            'title',
            'image',
        ]


class CustomUserSerializer(serializers.ModelSerializer):
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
