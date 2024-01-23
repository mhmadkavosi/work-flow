from django.urls import path
from . import views

urlpatterns = [
    path('leaves/', views.get_leaves)
]
