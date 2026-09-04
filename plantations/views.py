from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Plantation
from .forms import PlantationForm


@login_required
def liste_plantations(request):
    plantations = Plantation.objects.filter(utilisateur=request.user).order_by("-date_creation")
    return render(request, "plantations/liste.html", {"plantations": plantations})


@login_required
def creer_plantation(request):
    if request.method == "POST":
        form = PlantationForm(request.POST)
        if form.is_valid():
            plantation = form.save(commit=False)
            plantation.utilisateur = request.user
            plantation.save()
            messages.success(request, "Plantation créée avec succès.")
            return redirect("liste_plantations")
    else:
        form = PlantationForm()
    return render(request, "plantations/formulaire.html", {"form": form, "titre": "Nouvelle plantation"})


@login_required
def modifier_plantation(request, pk):
    plantation = get_object_or_404(Plantation, pk=pk, utilisateur=request.user)
    if request.method == "POST":
        form = PlantationForm(request.POST, instance=plantation)
        if form.is_valid():
            form.save()
            messages.success(request, "Plantation modifiée avec succès.")
            return redirect("liste_plantations")
    else:
        form = PlantationForm(instance=plantation)
    return render(request, "plantations/formulaire.html", {"form": form, "titre": "Modifier la plantation"})


@login_required
def detail_plantation(request, pk):
    plantation = get_object_or_404(Plantation, pk=pk, utilisateur=request.user)
    return render(request, "plantations/detail.html", {"plantation": plantation})

# Create your views here.
