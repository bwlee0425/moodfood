from django.urls import path
from . import views

urlpatterns = [
    path('mood/', views.mood_create, name='mood_create'),
]