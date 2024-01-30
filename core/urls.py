from django.urls import path
from . import views


urlpatterns = [
    path("", views.get_workflows),
    path('<int:pk>/', views.get_workflow),
    path("create/", views.create_workflow),
    path("step/create", views.create_step),
    path("request/create", views.create_request),
    path("request/update", views.update_request_status),
    path("request/reject", views.reject_request_status)
]
