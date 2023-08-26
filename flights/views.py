from rest_framework import viewsets

from flights.models import Crew
from flights.serializers import CrewSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

