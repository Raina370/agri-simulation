import re
from datetime import date
from django import forms


def valider_telephone(telephone):
    motif = r"^(\+237)?6\d{8}$"
    if telephone and not re.match(motif, telephone.replace(" ", "")):
        raise forms.ValidationError(
            "Numéro invalide. Format attendu : 6XXXXXXXX ou +2376XXXXXXXX."
        )
    return telephone


def valider_date_naissance(naissance):
    if naissance and naissance.year >= date.today().year:
        raise forms.ValidationError(
            "La date de naissance doit être antérieure à l'année en cours."
        )
    return naissance