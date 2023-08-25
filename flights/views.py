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


@api_view(["GET", "PUT", "DELETE"])
def crew_detail(request, pk):
    try:
        crew = Crew.objects.get(pk=pk)
    except Crew.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = CrewSerializer(crew)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CrewSerializer(crew, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        Crew.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)