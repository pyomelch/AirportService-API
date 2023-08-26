from django.urls import path, include

from rest_framework import routers

from flights.views import CrewViewSet

router = routers.DefaultRouter()
router.register("crews", CrewViewSet)

urlpatterns = [
   path("", include(router.urls))
]

app_name = "flights"
