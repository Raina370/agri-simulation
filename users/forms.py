import re
from django import forms
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur
from .validators import valider_telephone, valider_date_naissance

class InscriptionForm(UserCreationForm):
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = Utilisateur
        fields = [
             "last_name",
            "first_name",
            "date_naissance",
            "sexe",
            "region",
            "ville",
            "telephone",
            "email",
            "username",
            "description",
        ]
        widgets = {
            "date_naissance": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "last_name": "Nom",
            "first_name": "Prénom",
            "date_naissance": "Date de naissance",
            "sexe": "Sexe",
            "region": "Région",
            "ville": "Ville",
            "telephone": "Téléphone",
            "email": "Adresse email",
            "username": "Nom d'utilisateur",
            "description": "Description (optionnel)",
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Empêche de choisir une date dans l'année en cours ou future
        derniere_date_autorisee = date(date.today().year - 1, 12, 31)
        self.fields["date_naissance"].widget.attrs["max"] = derniere_date_autorisee.isoformat()

    def clean_date_naissance(self):
        naissance = self.cleaned_data.get("date_naissance")
        if naissance and naissance.year >= date.today().year:
            raise forms.ValidationError(
                "La date de naissance doit être antérieure à l'année en cours."
            )
        return naissance

    def clean_telephone(self):
        telephone = self.cleaned_data.get("telephone")
        motif = r"^(\+237)?6\d{8}$"
        if telephone and not re.match(motif, telephone.replace(" ", "")):
            raise forms.ValidationError(
                "Numéro invalide. Format attendu : 6XXXXXXXX ou +2376XXXXXXXX."
            )
        return telephone

REGIONS_CAMEROUN = [
    ("Adamaoua", "Adamaoua"), ("Centre", "Centre"), ("Est", "Est"),
    ("Extrême-Nord", "Extrême-Nord"), ("Littoral", "Littoral"), ("Nord", "Nord"),
    ("Nord-Ouest", "Nord-Ouest"), ("Ouest", "Ouest"), ("Sud", "Sud"), ("Sud-Ouest", "Sud-Ouest"),
]


class ProfilForm(forms.ModelForm):
    region = forms.ChoiceField(choices=REGIONS_CAMEROUN, label="Région")

    class Meta:
        model = Utilisateur
        fields = ["last_name", "first_name", "date_naissance", "sexe", "region", "ville", "telephone", "email", "description"]
        widgets = {
            "date_naissance": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Parlez de vous, de votre exploitation..."}),
        }
        labels = {
            "last_name": "Nom", "first_name": "Prénom", "date_naissance": "Date de naissance",
            "sexe": "Sexe", "ville": "Ville", "telephone": "Téléphone",
            "email": "Adresse email", "description": "Bio",
        }

    def clean_date_naissance(self):
        return valider_date_naissance(self.cleaned_data.get("date_naissance"))

    def clean_telephone(self):
        return valider_telephone(self.cleaned_data.get("telephone"))