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


class CustomUserSerizlier(serializers.ModelSerializer):
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
    user = CustomUserSerizlier(many=False)

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

