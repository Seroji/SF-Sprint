from django.urls import path, include

from .views import submitData

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'submitData', submitData)


urlpatterns = [
    # path('submitData', submitData.as_view()),
    path('', include(router.urls)),
]