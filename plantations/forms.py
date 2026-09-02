from django import forms
from django.utils import timezone
from .models import Plantation
from agriculture.models import Departement


class PlantationForm(forms.ModelForm):
    class Meta:
        model = Plantation
        fields = ["culture", "region", "departement", "sol", "superficie", "date_plantation"]
        widgets = {
            "date_plantation": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "culture": "Culture",
            "region": "Région",
            "departement": "Département",
            "sol": "Type de sol",
            "superficie": "Superficie (hectares)",
            "date_plantation": "Date de plantation prévue",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date_plantation"].widget.attrs["min"] = timezone.now().date().isoformat()

    def clean_superficie(self):
        superficie = self.cleaned_data.get("superficie")
        if superficie is not None and superficie <= 0:
            raise forms.ValidationError("La superficie doit être supérieure à 0.")
        return superficie