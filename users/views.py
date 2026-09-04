from django.shortcuts import render, redirect
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
from .forms import InscriptionForm, ProfilForm
from plantations.models import Plantation


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
        username = request.POST.get("username")
        password = request.POST.get("password")
        utilisateur = authenticate(request, username=username, password=password)
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
    return render(request, "users/dashboard_agriculteur.html", {
        "nb_simulations": nb_simulations,
        "culture_top": culture_top,
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
def dashboard_admin(request):
    if not request.user.is_staff:
        return redirect("dashboard_agriculteur")
    return render(request, "users/dashboard_admin.html")


# Create your views here.
