from django.urls import path
from services import views
app_name = "services"


urlpatterns = [
    path("indications/<int:apartment_id>/", views.indications_view, name="indications"),
    path("last_entry/<int:apartment_id>/", views.profile_last_entry, name="last_entry"),
    path("tables/<int:apartment_id>/", views.tables, name="tables"),
]
