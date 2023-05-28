from rest_framework import views
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

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
        name = request.data.get('user_info')
        last_name, first_name, patronymic = name.split(" ")
        data = request.data
        data.pop('user_info')
        user = {'user': 
                {
            "email": request.data.get('email'),
            "last_name": last_name,
            "first_name": first_name,
            "patronymic": patronymic,
            "phone": request.data.get('phone'),
                }
        }
        height = request.data.pop('height')
        latitude = request.data.pop('latitude')
        longitude = request.data.pop('longitude')
        coords = {
            'height': height,
            "latitude": latitude,
            "longitude": longitude,
        }
        data['coords'] = coords
        data['user'] = user
        serializer = PerevalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response('Success!')
        print(serializer.errors)
        return Response(serializer.data)


