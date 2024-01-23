from django.urls import path
from . import views

BASE_URL = 'leaves'


urlpatterns = [
    path(f"{BASE_URL}/", views.get_leaves),
    path(f"{BASE_URL}/<int:id>/", views.get_leaves_info),
    path(f"{BASE_URL}/create", views.create_leaves),
    path(f"{BASE_URL}/update-status", views.update_leave_status),
]
