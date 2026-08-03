from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_volunteer, name="register_volunteer"),
    path("organizations/", views.organization_list, name="organization_list"),
    path("organizations/create/", views.create_organization, name="create_organization"),
    path("organizations/<int:organization_id>/", views.organization_detail, name="organization_detail"),
    path("animals/", views.animal_list, name="animal_list"),
    path("organizations/<int:organization_id>/edit/", views.edit_organization, name="edit_organization"),
    path("organizations/<int:organization_id>/delete/", views.delete_organization, name="delete_organization"),
    path("organizations/<int:organization_id>/volunteers/", views.organization_volunteers, name="organization_volunteers"),
    path("organizations/<int:organization_id>/bank-statements/", views.bank_statement_list, name="bank_statement_list"),
    path("organizations/<int:organization_id>/bank-statements/upload/", views.upload_bank_statement, name="upload_bank_statement"),
    path("animals/add/<int:organization_id>/", views.add_animal, name="add_animal"),
    path("animals/<int:animal_id>/edit/", views.edit_animal, name="edit_animal"),
    path("animals/<int:animal_id>/delete/", views.delete_animal, name="delete_animal"),
    path("animals/<int:animal_id>/", views.animal_detail, name="animal_detail"),
    path("animals/<int:animal_id>/foster/", views.foster_animal, name="foster_animal"),
    path("animals/<int:animal_id>/request/", views.submit_adoption_request, name="submit_adoption_request"),
    path("requests/", views.request_list, name="request_list"),
    path("requests/<int:request_id>/", views.request_detail, name="request_detail"),
    path("requests/<int:request_id>/close/", views.close_request, name="close_request"),
    path("adopters/", views.adopter_list, name="adopter_list"),
    path("adopters/add/", views.add_adopter, name="add_adopter"),
    path("system/users/", views.system_users, name="system_users"),
    path("initialize/", views.initialize_data, name="initialize_data"),
]
