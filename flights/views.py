from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from flights.models import Crew
from flights.serializers import CrewSerializer


@api_view(["GET", "POST"])
def crew_list(request):
    if request.method == "GET":
        crews = Crew.objects.all()
        serializer = CrewSerializer(crews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "POST":
        serializer = CrewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
