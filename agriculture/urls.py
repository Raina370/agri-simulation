from django.urls import path
from . import views

urlpatterns = [
    path("cultures/", views.liste_cultures, name="admin_cultures"),
    path("cultures/nouvelle/", views.creer_culture, name="admin_creer_culture"),
    path("cultures/<int:pk>/modifier/", views.modifier_culture, name="admin_modifier_culture"),
    path("cultures/<int:pk>/supprimer/", views.supprimer_culture, name="admin_supprimer_culture"),
    path("sols/", views.liste_sols, name="admin_sols"),
    path("sols/nouveau/", views.creer_sol, name="admin_creer_sol"),
    path("sols/<int:pk>/modifier/", views.modifier_sol, name="admin_modifier_sol"),
    path("sols/<int:pk>/supprimer/", views.supprimer_sol, name="admin_supprimer_sol"),
]