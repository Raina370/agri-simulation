from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Plantation
from .forms import PlantationForm
from simulation.moteur import calculer_simulation
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


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
    resultat = calculer_simulation(plantation)
    resultat_objet = plantation.resultat
    return render(request, "plantations/detail.html", {
        "plantation": plantation,
        "resultat": resultat,
        "risques": resultat_objet.risques.all(),
        "recommandations": resultat_objet.recommandations.all(),
    })

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

@login_required
def telecharger_pdf(request, pk):
    plantation = get_object_or_404(Plantation, pk=pk, utilisateur=request.user)
    resultat_objet = plantation.resultat

    template = get_template("plantations/rapport_pdf.html")
    html = template.render({
        "plantation": plantation,
        "resultat": resultat_objet,
        "risques": resultat_objet.risques.all(),
        "recommandations": resultat_objet.recommandations.all(),
    })

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="simulation_{plantation.nom_parcelle}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Erreur lors de la génération du PDF", status=500)

    return response

@login_required
def liste_plantations(request):
    plantations = Plantation.objects.filter(utilisateur=request.user).order_by("-date_creation")
    return render(request, "plantations/liste.html", {"plantations": plantations})

@login_required
def supprimer_plantation(request, pk):
    plantation = get_object_or_404(Plantation, pk=pk, utilisateur=request.user)
    if request.method == "POST":
        plantation.delete()
    return redirect("liste_plantations")