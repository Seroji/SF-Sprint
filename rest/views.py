from rest_framework import views
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from django.http import JsonResponse
from django.core.exceptions import ValidationError

from .models import PerevalAdded
from .serializers import PerevalSerializer


class submitData(views.APIView):
    @extend_schema(
            request=PerevalSerializer,
            responses=PerevalSerializer,
            examples=[
                OpenApiExample(
                'Post example',
                    value=
                    {
                        "height": "1200",
                        "longitude": "48.068",
                        "latitude": "120.087",
                        "title": "пер.",
                        "beauty_title": "Пхия",
                        "other_titles": "Триев",
                        "images": [
                            {"image":"<img1>", "title":"Седловина"}, 
                            {"image":"<img2>", "title":"Подъём"}
                            ],
                        "user_info": "Иванов Иван Иванович",
                        "email": "example@mail.ru",
                        "phone": "9843345676",
                        "level" : {
                            'winter': "1A",
                            "spring": "",
                            "summer": "",
                            "autumn": "1A",
                        }
                    }
                )
            ]
    )
    def post(self, request):
        data = request.data
        name = data.pop('user_info')
        last_name, first_name, patronymic = name.split(" ")
        height = request.data.pop('height')
        latitude = request.data.pop('latitude')
        longitude = request.data.pop('longitude')
        user = {
            "email": request.data.get('email'),
            "last_name": last_name,
            "first_name": first_name,
            "patronymic": patronymic,
            "phone": request.data.get('phone'),
        }
        coords = {
            'height': height,
            "latitude": latitude,
            "longitude": longitude,
            "email": request.data.pop('email'),
            "phone": request.data.pop('phone'),
        }
        data['coords'] = coords
        data['user'] = user
        serializer = PerevalSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.errors)
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        print(serializer.errors)
        return Response(serializer.data)
