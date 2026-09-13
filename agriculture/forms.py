from django import forms
from .models import Culture, Sol


class CultureForm(forms.ModelForm):
    class Meta:
        model = Culture
        fields = ["nom", "cycle_jours", "pluviometrie_min", "pluviometrie_max",
                  "temperature_min", "temperature_max", "rendement_reference", "sols_compatibles"]
        widgets = {
                    "sols_compatibles": forms.CheckboxSelectMultiple,
                   "rendement_reference": forms.NumberInput(attrs={"class": "form-control"}),}


class SolForm(forms.ModelForm):
    class Meta:
        model = Sol
        fields = ["type_sol", "description", "ph_moyen"]