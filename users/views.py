from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm
from agriculture.models import Culture
from django.utils.text import slugify
from django.db.models import Count
from plantations.models import Plantation
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.db.models import Sum, Count
from .forms import InscriptionForm, ProfilForm, AdminUtilisateurForm
from plantations.models import Plantation
from django.db.models import Count, Avg
from django.contrib.auth import get_user_model
from .decorators import admin_required
from plantations.models import Plantation
from chatbot.models import Conversation

def demarrage(request):
    return render(request, "demarrage.html")

def accueil(request):
    cultures = Culture.objects.all()
    cultures_avec_images = [
        {"culture": culture, "image": f"images/cultures/{slugify(culture.nom)}.png"}
        for culture in cultures
    ]
    return render(request, "users/accueil.html", {"cultures_avec_images": cultures_avec_images})

def inscription(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            utilisateur = form.save()
            login(request, utilisateur)
            messages.success(request, "Inscription réussie, bienvenue !")
            return redirect("dashboard")
    else:
        form = InscriptionForm()
    return render(request, "users/inscription.html", {"form": form})


def connexion(request):
    if request.method == "POST":
        username = request.POST.get("username","" ).strip()
        mot_de_passe = request.POST.get("password","" ).strip()
        utilisateur = authenticate(request, username = username, password = mot_de_passe)
        if utilisateur is not None:
            login(request, utilisateur)
            return redirect("dashboard")
        else:
            messages.error(request, "Identifiants incorrects.")
    return render(request, "users/connexion.html")


def deconnexion(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect("connexion")


@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect("dashboard_admin")
    return redirect("dashboard_agriculteur")


@login_required
def dashboard_agriculteur(request):
    plantations = Plantation.objects.filter(utilisateur=request.user)
    nb_simulations = plantations.count()

    culture_top = (
        plantations.values("culture__nom")
        .annotate(total=Count("culture"))
        .order_by("-total")
        .first()
    )

    dernieres = plantations.order_by("-date_creation")[:3]

    rendement_moyen = plantations.filter(resultat__isnull=False).aggregate(
        moyenne=Avg("resultat__rendement_estime")
    )["moyenne"]

    return render(request, "users/dashboard_agriculteur.html", {
        "nb_simulations": nb_simulations,
        "culture_top": culture_top,
        "rendement_moyen": round(rendement_moyen, 2) if rendement_moyen else None,
        "dernieres": dernieres
    })
@login_required
def profil(request):
    plantations = Plantation.objects.filter(utilisateur=request.user)
    superficie_totale = plantations.aggregate(total=Sum("superficie"))["total"]
    cultures_principales = (
        plantations.values("culture__nom")
        .annotate(total=Count("culture"))
        .order_by("-total")[:5]
    )
    return render(request, "users/profil.html", {
        "superficie_totale": superficie_totale,
        "cultures_principales": cultures_principales,
    })


@login_required
def profil_modifier(request):
    if request.method == "POST":
        form = ProfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect("profil")
    else:
        form = ProfilForm(instance=request.user)
    return render(request, "users/profil_modifier.html", {"form": form})


class ChangerMotDePasseView(PasswordChangeView):
    template_name = "users/mot_de_passe.html"
    success_url = reverse_lazy("mot_de_passe_confirme")


class MotDePasseConfirmeView(PasswordChangeDoneView):
    template_name = "users/mot_de_passe_confirme.html"


@login_required
@admin_required
def dashboard_admin(request):
    Utilisateur = get_user_model()
    from agriculture.models import Culture

    stats = {
        "nb_utilisateurs": Utilisateur.objects.filter(is_staff=False).count(),
        "nb_admins": Utilisateur.objects.filter(is_staff=True).count(),
        "nb_simulations": Plantation.objects.count(),
        "nb_cultures": Culture.objects.count(),
        "nb_conversations": Conversation.objects.count(),
    }
    derniers_utilisateurs = Utilisateur.objects.filter(is_staff=False).order_by("-date_joined")[:5]

    return render(request, "users/dashboard_admin.html", {
        "stats": stats,
        "derniers_utilisateurs": derniers_utilisateurs,
    })


@admin_required
def admin_liste_utilisateurs(request):
    Utilisateur = get_user_model()
    utilisateurs = Utilisateur.objects.filter(is_staff=False).order_by("-date_joined")
    return render(request, "users/admin_utilisateurs_liste.html", {"utilisateurs": utilisateurs})


@admin_required
def admin_detail_utilisateur(request, pk):
    Utilisateur = get_user_model()
    utilisateur_cible = get_object_or_404(Utilisateur, pk=pk)
    nb_simulations = Plantation.objects.filter(utilisateur=utilisateur_cible).count()

    if request.method == "POST":
        if "toggle_actif" in request.POST:
            utilisateur_cible.is_active = not utilisateur_cible.is_active
            utilisateur_cible.save()
            messages.success(request, f"Compte {'activé' if utilisateur_cible.is_active else 'désactivé'}.")
        elif "toggle_staff" in request.POST:
            utilisateur_cible.is_staff = not utilisateur_cible.is_staff
            utilisateur_cible.save()
            messages.success(request, "Statut administrateur mis à jour.")
        return redirect("admin_detail_utilisateur", pk=pk)

    return render(request, "users/admin_utilisateur_detail.html", {
        "utilisateur_cible": utilisateur_cible,
        "nb_simulations": nb_simulations,
    })
@admin_required
def admin_ajouter_utilisateur(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)

        if form.is_valid():
            utilisateur = form.save()
            messages.success(
                request,
                f"Le compte de {utilisateur.get_full_name() or utilisateur.username} a été créé avec succès."
            )
            return redirect("admin_utilisateurs")

    else:
        form = InscriptionForm()

    return render(
        request,
        "users/admin_utilisateur_form.html",
        {
            "form": form,
            "mode": "ajouter",
        }
    )


@admin_required
def admin_modifier_utilisateur(request, pk):
    Utilisateur = get_user_model()
    utilisateur_cible = get_object_or_404(Utilisateur, pk=pk)

    if request.method == "POST":
        form = AdminUtilisateurForm(
            request.POST,
            instance=utilisateur_cible
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Les informations de l'utilisateur ont été mises à jour avec succès."
            )

            return redirect(
                "admin_detail_utilisateur",
                pk=utilisateur_cible.pk
            )

    else:
        form = AdminUtilisateurForm(
            instance=utilisateur_cible
        )

    return render(
        request,
        "users/admin_utilisateur_form.html",
        {
            "form": form,
            "utilisateur_cible": utilisateur_cible,
            "mode": "modifier",
        }
    )


@admin_required
def admin_supprimer_utilisateur(request, pk):
    Utilisateur = get_user_model()
    utilisateur_cible = get_object_or_404(Utilisateur, pk=pk)
    if request.method == "POST":
        utilisateur_cible.delete()
        messages.success(request, "Utilisateur supprimé.")
    return redirect("admin_utilisateurs")

# Create your views here.
