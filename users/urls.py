from django.urls import path
from . import views

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("inscription/", views.inscription, name="inscription"),
    path("connexion/", views.connexion, name="connexion"),
    path("deconnexion/", views.deconnexion, name="deconnexion"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/agriculteur/", views.dashboard_agriculteur, name="dashboard_agriculteur"),
    path("dashboard/admin/", views.dashboard_admin, name="dashboard_admin"),
]