from django import forms
from django.utils import timezone
from .models import Plantation
from agriculture.models import Region, Departement, Sol


class SelectRegionRestreinte(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value and str(label) != "Ouest":
            option["attrs"]["disabled"] = "disabled"
        return option


class PlantationForm(forms.ModelForm):
    class Meta:
        model = Plantation
        fields = ["nom_parcelle", "culture", "region", "departement", "sol", "superficie", "date_plantation"]
        widgets = {
            "nom_parcelle": forms.TextInput(attrs={"placeholder": "Ex: Champ Ouest"}),
            "culture": forms.RadioSelect,
            "region": SelectRegionRestreinte,
            "date_plantation": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "nom_parcelle": "Nom de la parcelle",
            "culture": "Type de culture principale",
            "region": "Région",
            "departement": "Département",
            "sol": "Type de sol",
            "superficie": "Superficie (hectares)",
            "date_plantation": "Date de plantation",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["region"].queryset = Region.objects.all().order_by("nom")

        region_ouest = Region.objects.filter(nom="Ouest").first()
        if region_ouest:
            self.fields["region"].initial = region_ouest
            self.fields["departement"].queryset = Departement.objects.filter(region=region_ouest).order_by("nom")

        self.fields["sol"].queryset = Sol.objects.all().order_by("type_sol")
        self.fields["date_plantation"].widget.attrs["min"] = timezone.now().date().isoformat()

    def clean_superficie(self):
        superficie = self.cleaned_data.get("superficie")
        if superficie is not None and superficie <= 0:
            raise forms.ValidationError("La superficie doit être supérieure à 0.")
        return superficie

    def clean_region(self):
        region = self.cleaned_data.get("region")
        if region and region.nom != "Ouest":
            raise forms.ValidationError("Seule la région de l'Ouest est disponible pour l'instant.")
        return region