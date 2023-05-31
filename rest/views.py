from rest_framework import views, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from django.http import JsonResponse
from django.core.exceptions import ValidationError

from .models import PerevalAdded, Coords, Status
from .serializers import PerevalSerializer
from .exceptions import DBWriteError


class submitData(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalSerializer

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
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = PerevalSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            obj_id = self.get_new_id(data=data)
            return Response({"status": status.HTTP_200_OK, "message": "null", "id": f"{obj_id}"}, status=status.HTTP_200_OK)
        raise DBWriteError({"message": "Ошибка записи в базу данных"})
    
    def get_new_id(self, data):
        coords = data.pop('coords')
        obj_coords = Coords.objects.get(**coords)
        obj = PerevalAdded.objects.get(coords=obj_coords)
        return obj.id

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        status_id = instance.status_id
        data = serializer.data
        data['status'] = Status.objects.get(id=status_id).title
        return Response(data)