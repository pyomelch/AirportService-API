from django.urls import path

from flights.views import CrewList, CrewDetail

urlpatterns = [
   path("crews/", CrewList.as_view(), name="crew-list"),
   path("crews/<int:pk>/", CrewDetail.as_view(), name="crew-detail"),
]

app_name = "flights"
