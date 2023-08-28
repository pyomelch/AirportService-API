from django.urls import path, include

from rest_framework import routers

from flights.views import (
   CrewViewSet,
   AirplaneTypeViewSet,
   AirplaneViewSet,
   AirportViewSet,
   RouteViewSet,
   FlightViewSet,
   OrderViewSet,
)


router = routers.DefaultRouter()
router.register("crews", CrewViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("flights", FlightViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
   path("", include(router.urls))
]

app_name = "flights"
