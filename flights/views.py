from django.http import JsonResponse

from flights.models import Crew
from flights.serializers import CrewSerializer


def crew_list(request):
    if request.method == "GET":
        crews = Crew.objects.all()
        serializer = CrewSerializer(crews, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)

