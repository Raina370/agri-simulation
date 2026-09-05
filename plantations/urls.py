from django.urls import path
from . import views

urlpatterns = [
    path("nouvelle/", views.creer_plantation, name="creer_plantation"),
    path("<int:pk>/", views.detail_plantation, name="detail_plantation"),
    path("<int:pk>/modifier/", views.modifier_plantation, name="modifier_plantation"),
    path("<int:pk>/confirmation/", views.simulation_confirmation, name="simulation_confirmation"),
    path("<int:pk>/", views.detail_plantation, name="detail_plantation"),
]