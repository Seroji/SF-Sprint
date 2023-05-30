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
                        "beauty_title": "пер. ",
                        "title": "Пхия",
                        "other_titles": "Триев",
                        "connect": "",
                        "add_time": "2021-09-22 13:18:13",
                        "user": {
                            "email": "qwerty@mail.ru", 		
                            "fam": "Пупкин",
                            "name": "Василий",
                            "otc": "Иванович",
                            "phone": "+7 555 55 55"
                            },
                        "coords":{
                            "latitude": "45.3842",
                            "longitude": "7.1525",
                            "height": "1200"
                            },
                        "level":{
                            "winter": "",
                            "summer": "1A",
                            "autumn": "1A",
                            "spring": ""
                            },
                        "images": [
                            {"image":"<картинка1>", "title":"Седловина"}, 
                            {"image":"<картинка>", "title":"Подъём"}
                            ]
                    }
                )
            ]
    )
    def post(self, request):
        data = request.data
        name = data.pop('user_info')
        lst = name.split(' ')
        if len(lst) < 3:
            return Response({'status': 500, 'message': 'Поле ФИО некорректно'})
        last_name, first_name, patronymic = lst
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
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return Response(serializer.data)
