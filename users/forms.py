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
    "last_name", "first_name",  
     "telephone",  "username",
]
        
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
            
        }

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
class AdminUtilisateurForm(forms.ModelForm):
    region = forms.ChoiceField(choices=REGIONS_CAMEROUN, label="Région")

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
            "description",
            "username",
        ]
        widgets = {
            "date_naissance": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Parlez de vous, de votre exploitation..."
                }
            ),
        }
        labels = {
            "last_name": "Nom",
            "first_name": "Prénom",
            "date_naissance": "Date de naissance",
            "sexe": "Sexe",
            "ville": "Ville",
            "telephone": "Téléphone",
            "description": "Bio",
            "username": "Nom d'utilisateur",
        }

        help_texts = {
            "username": "",
        }
    def clean_date_naissance(self):
        return valider_date_naissance(
            self.cleaned_data.get("date_naissance")
        )

    def clean_telephone(self):
        return valider_telephone(
            self.cleaned_data.get("telephone")
        )