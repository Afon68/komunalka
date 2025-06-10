from django.urls import path
from apartaments import views
app_name = 'apartaments'


urlpatterns = [
    path("add_apartment/", views.add_apartment, name="add_apartment"),
    path("user_objects/<int:apartment_id>/", views.del_apartment, name="user_objects"),
    path("user_objects/", views.UserObjectsView.as_view(), name="user_objects"),
    path("apartment_profile/<int:apartment_id>/", views.apartment_profile, name="apartment_profile"),
    path("edit_apartment/<int:apartment_id>/", views.edit_apartment, name="edit_apartment"),
]
