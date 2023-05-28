from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import (Coords,
                     Level,
                     Image,
                     PerevalAdded,
                     CustomUser)


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


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
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        patronymic = validated_data.pop('patronymic')
        CustomUser.objects.create(
            fisrt_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            email=validated_data.pop('email'),
            phone=validated_data.pop('phone'),
        )
        Coords.objects.create(
            height=validated_data.pop('height'),
            logitude=validated_data.pop('logitude'),
            latitude=validated_data.pop('latitude'),
        )
        for image in validated_data.pop('images'):
            Image.objects.create(
                title=image.pop('title'),
                image=image.pop('data')
            )
        level = validated_data.pop('level')
        Level.objects.create(
            winter=level.pop('winter'),
            spring=level.pop('spring'),
            summer=level.pop('summer'),
            autumn=level.pop('autumn'),
        )
        pereval = PerevalAdded.objects.create(**validated_data)
        return pereval

