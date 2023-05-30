from rest_framework import views
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from django.http import JsonResponse
from django.core.exceptions import ValidationError

from .models import PerevalAdded
from .serializers import PerevalSerializer
from .exceptions import DBWriteError


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
                            "last_name": "Пупкин",
                            "first_name": "Василий",
                            "patronymic": "Иванович",
                            "phone": "+7 953 212 64 78"
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
                            {"image":"<картинка2>", "title":"Подъём"}
                            ]
                    }
                )
            ]
    )
    def post(self, request):
        data = request.data
        serializer = PerevalSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response()
        raise DBWriteError({"message": "Ошибка записи в базу данных"})
