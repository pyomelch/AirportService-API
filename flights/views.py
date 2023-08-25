from rest_framework import mixins, viewsets

from flights.models import Crew
from flights.serializers import CrewSerializer


class CrewViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

