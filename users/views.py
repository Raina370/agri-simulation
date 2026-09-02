from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm
from agriculture.models import Culture
from django.utils.text import slugify

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
    return render(request, "users/dashboard_agriculteur.html")


@login_required
def dashboard_admin(request):
    if not request.user.is_staff:
        return redirect("dashboard_agriculteur")
    return render(request, "users/dashboard_admin.html")


# Create your views here.
