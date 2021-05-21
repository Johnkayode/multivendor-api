from django.urls import path

from .views import ListandCreateAdmin



urlpatterns = [
    path('', ListandCreateAdmin.as_view(), name='list_and_create_admin'),
]