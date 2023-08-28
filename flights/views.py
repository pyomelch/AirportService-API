from datetime import datetime

from django.db.models import Count, F
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from flights.models import (
    Crew,
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Flight,
    Order,
)
from flights.serializers import (
    CrewSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirportSerializer,
    RouteSerializer,
    FlightSerializer,
    OrderSerializer,
    AirplaneListSerializer,
    RouteListSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    OrderListSerializer,
)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("type")
    serializer_class = AirplaneSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        return AirplaneSerializer

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get("name")
        type = self.request.query_params.get("type")
        if name:
            queryset = queryset.filter(airplane_name__icontains=name)

        if type:
            queryset = queryset.filter(type__airplane_type__icontains=type)

        return queryset

    def list(self, request, *args, **kwargs):
        return super(AirplaneViewSet, self).list(request, *args, **kwargs)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related(
        "source",
        "destination"
    )
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        return RouteSerializer

    def get_queryset(self):
        queryset = self.queryset
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        if source:
            queryset = queryset.filter(
                source__closest_big_city__icontains=source
            )

        if destination:
            queryset = queryset.filter(
                destination__closest_big_city__icontains=destination
            )

        return queryset

    def list(self, request, *args, **kwargs):
        return super(RouteViewSet, self).list(request, *args, **kwargs)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related(
        "airplane",
        "route__source",
        "route__destination"
    )
    serializer_class = FlightSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer

    def get_queryset(self):
        queryset = self.queryset
        date = self.request.query_params.get("date")
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")
        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(departure_time__date=date)
        if source:
            queryset = queryset.filter(
                route__source__name__icontains=source
            )
        if destination:
            queryset = queryset.filter(
                route__destination__name__icontains=destination
            )
        if self.action == "list":
            queryset = queryset.annotate(
                tickets_available=(
                        F("airplane__rows") * F("airplane__seats_in_row")
                        - Count("tickets")
                )
            )
        if self.action == "retrieve":
            queryset = queryset.prefetch_related("crew")

        return queryset

    def list(self, request, *args, **kwargs):
        return super(FlightViewSet, self).list(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        if self.action == "list":
            queryset = queryset.prefetch_related(
                "tickets__flight__airplane",
                "tickets__flight__route__source",
                "tickets__flight__route__destination",
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAdminUser()]

        return super(OrderViewSet, self).get_permissions()