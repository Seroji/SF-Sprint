from rest_framework import views
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from .models import PerevalAdded
from .serializers import PerevalSerializer


class submitData(views.APIView):
    @extend_schema(
            request=PerevalSerializer,
            responses=PerevalSerializer,
    )
    def post(self, request):
        pereval_serializer = PerevalSerializer(data=request.data)
        return Response({'total': 'Success!'})

