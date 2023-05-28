from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import (Coords,
                     Level,
                     Image,
                     PerevalAdded)


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
        models = Image
        fields = '__all__'


class PerevalSerializers(serializers.ModelSerializer):
    coords = CoordsSerializer(many=True)
    level = LevelSerializer(many=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = PerevalAdded
        fields = '__all__'

    # def create(self, validated_data):
