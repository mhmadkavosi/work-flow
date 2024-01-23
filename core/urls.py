from django.urls import path
from . import views


urlpatterns = [
    path("", views.get_workflows),
    path('<int:pk>/', views.get_workflow)
]
