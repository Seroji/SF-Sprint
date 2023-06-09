from rest_framework import views, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, extend_schema_view
from drf_spectacular.types import OpenApiTypes

from django.http import JsonResponse
from django.core.exceptions import ValidationError

from .models import PerevalAdded, Coords, Status
from .serializers import PerevalSerializer
from .exceptions import DBWriteError


class submitData(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet,
                   mixins.ListModelMixin):
    serializer_class = PerevalSerializer
    http_method_names = ['get', 'post', 'patch']

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
            ],
            summary="Add information about new PEREVAL via POST request.",
            description=
            """
            Add informamation about new PEREVAL via POST request. It requires JSON request like in the example below.
            Pay your attention to the format of all the fields. If coords already exist in the database, it will cause error.
            If user is already in the database, new user won't be added in the database, however information about new PEREVAL will be added
            and connected with the existing user.
            """
    )
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = PerevalSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            obj_id = self.get_id(data=data)
            return Response({"status": status.HTTP_200_OK, "message": "null", "id": f"{obj_id}"}, status=status.HTTP_200_OK)
        raise DBWriteError({"message": "Ошибка записи в базу данных"})
    
    def get_id(self, data):
        coords = data.pop('coords')
        obj_coords = Coords.objects.get(**coords)
        obj = PerevalAdded.objects.get(coords=obj_coords)
        return obj.id
    
    @extend_schema(
            responses=PerevalSerializer,
            summary="Get PEREVAL but its id.",
            description=
            """
            You need to pass value of the id of PERAVAL via URL. The type of id is integer. 
            EXAMPLE: .../submitData/1/ 
            """
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        status_id = instance.status_id
        data = serializer.data
        data['status'] = Status.objects.get(id=status_id).title
        return Response(data)
    
    @extend_schema(
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
            ],
            summary='Make partial update of an information about the PEREVAL',
            description=
            """
            You need to pass JSON request like in the example below. You can't edit any information about the user,
            the programm will skip that. However variance of another data is possible.
            """
    )
    def partial_update(self, request, *args, **kwargs):
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.status_id != 1:
            return Response({"state": 0, "message": "Статус объекта не позволяет осуществлять редактирование"})

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({"state": 1, "message": "null"})
    
    @extend_schema(
            request=PerevalSerializer,
            responses=PerevalSerializer,
            parameters=[
                OpenApiParameter(name='user_email', location=OpenApiParameter.QUERY),
            ],
            summary="Get LIST of PEREVALs.",
            description=
            """
            Without any query params it will return to you information about all the PEREVALs in the database.
            However if you pass user_email query param, you'll get all PEREVALs which is connected with the user with 
            this email.
            """
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
        queryset = PerevalAdded.objects.all()
        email = self.request.query_params.get('user_email')
        if email:
            queryset = queryset.filter(user__email=email)
        return queryset