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
    path("profil/", views.profil, name="profil"),
    path("profil/modifier/", views.profil_modifier, name="profil_modifier"),
    path("profil/mot-de-passe/", views.ChangerMotDePasseView.as_view(), name="mot_de_passe"),
    path("profil/mot-de-passe/confirme/", views.MotDePasseConfirmeView.as_view(), name="mot_de_passe_confirme"),
]