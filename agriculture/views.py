from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.decorators import admin_required
from .models import Culture, Sol
from .forms import CultureForm, SolForm


@admin_required
def liste_cultures(request):
    cultures = Culture.objects.all().order_by("nom")
    return render(request, "agriculture/liste_cultures.html", {"cultures": cultures})


@admin_required
def creer_culture(request):
    if request.method == "POST":
        form = CultureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Culture créée avec succès.")
            return redirect("admin_cultures")
    else:
        form = CultureForm()
    return render(request, "agriculture/form_culture.html", {"form": form, "titre": "Nouvelle culture"})


@admin_required
def modifier_culture(request, pk):
    culture = get_object_or_404(Culture, pk=pk)
    if request.method == "POST":
        form = CultureForm(request.POST, instance=culture)
        if form.is_valid():
            form.save()
            messages.success(request, "Culture mise à jour.")
            return redirect("admin_cultures")
    else:
        form = CultureForm(instance=culture)
    return render(request, "agriculture/form_culture.html", {"form": form, "titre": "Modifier la culture"})


@admin_required
def supprimer_culture(request, pk):
    culture = get_object_or_404(Culture, pk=pk)
    if request.method == "POST":
        culture.delete()
        messages.success(request, "Culture supprimée.")
    return redirect("admin_cultures")


@admin_required
def liste_sols(request):
    sols = Sol.objects.all().order_by("type_sol")
    return render(request, "agriculture/liste_sols.html", {"sols": sols})


@admin_required
def creer_sol(request):
    if request.method == "POST":
        form = SolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sol créé avec succès.")
            return redirect("admin_sols")
    else:
        form = SolForm()
    return render(request, "agriculture/form_sol.html", {"form": form, "titre": "Nouveau type de sol"})


@admin_required
def modifier_sol(request, pk):
    sol = get_object_or_404(Sol, pk=pk)
    if request.method == "POST":
        form = SolForm(request.POST, instance=sol)
        if form.is_valid():
            form.save()
            messages.success(request, "Sol mis à jour.")
            return redirect("admin_sols")
    else:
        form = SolForm(instance=sol)
    return render(request, "agriculture/form_sol.html", {"form": form, "titre": "Modifier le type de sol"})


@admin_required
def supprimer_sol(request, pk):
    sol = get_object_or_404(Sol, pk=pk)
    if request.method == "POST":
        sol.delete()
        messages.success(request, "Sol supprimé.")
    return redirect("admin_sols")

# Create your views here.
