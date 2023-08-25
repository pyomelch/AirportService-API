from django.urls import path

from flights.views import CrewViewSet

crew_list = CrewViewSet.as_view(actions={"get": "list", "post": "create"})
crew_detail = CrewViewSet.as_view(actions={
   "get": "retrieve",
   "put": "update",
   "patch": "partial_update",
   "delete": "destroy",
})

urlpatterns = [
   path("crews/", crew_list, name="crew-list"),
   path("crews/<int:pk>/", crew_detail, name="crew-detail"),
]

app_name = "flights"
