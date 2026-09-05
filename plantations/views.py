from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Plantation
from .forms import PlantationForm


@login_required
def creer_plantation(request):
    plantation_creee = None
    if request.method == "POST":
        form = PlantationForm(request.POST)
        if form.is_valid():
            plantation = form.save(commit=False)
            plantation.utilisateur = request.user
            plantation.save()
            plantation_creee = plantation
            form = PlantationForm()
    else:
        form = PlantationForm()
    return render(request, "plantations/formulaire.html", {
        "form": form,
        "plantation_creee": plantation_creee,
    })

@login_required
def simulation_confirmation(request, pk):
    plantation = get_object_or_404(Plantation, pk=pk, utilisateur=request.user)
    return render(request, "plantations/confirmation.html", {"plantation": plantation})


@login_required
def detail_plantation(request, pk):
    plantation = get_object_or_404(Plantation, pk=pk, utilisateur=request.user)
    return render(request, "plantations/detail.html", {"plantation": plantation})

@login_required
def modifier_plantation(request, pk):
    plantation = get_object_or_404(Plantation, pk=pk, utilisateur=request.user)
    if request.method == "POST":
        form = PlantationForm(request.POST, instance=plantation)
        if form.is_valid():
            form.save()
            return redirect("detail_plantation", pk=plantation.pk)
    else:
        form = PlantationForm(instance=plantation)
    return render(request, "plantations/formulaire.html", {"form": form, "titre": "Modifier la simulation"})