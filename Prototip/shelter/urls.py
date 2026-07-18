from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("animals/", views.animal_list, name="animal_list"),
    path("animals/<int:animal_id>/", views.animal_detail_view, name="animal_detail"),
    path("animals/adopted/", views.adopted_animals_list, name="adopted_animals_list"),
    path("requests/", views.request_list_view, name="request_list"),
    path("requests/<int:request_id>/", views.request_detail_view, name="request_detail"),
    path("requests/<int:request_id>/close/", views.close_request_view, name="close_request"),
    path("animals/<int:animal_id>/return/", views.return_animal_view, name="return_animal"),
]
