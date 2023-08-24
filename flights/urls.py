from django.urls import path

from flights.views import crew_list

urlpatterns = [
   path("crews/", crew_list, name="crew-list")
]

app_name = "flights"
