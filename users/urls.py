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
    path("gestion/utilisateurs/", views.admin_liste_utilisateurs, name="admin_utilisateurs"),
    path("gestion/utilisateurs/<int:pk>/", views.admin_detail_utilisateur, name="admin_detail_utilisateur"),
    path("gestion/utilisateurs/<int:pk>/supprimer/", views.admin_supprimer_utilisateur, name="admin_supprimer_utilisateur"),
    path("gestion/utilisateurs/ajouter/",views.admin_ajouter_utilisateur,name="admin_ajouter_utilisateur"),
    path("gestion/utilisateurs/<int:pk>/modifier/",views.admin_modifier_utilisateur,name="admin_modifier_utilisateur"),
]