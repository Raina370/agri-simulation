from django.db import models
from plantations.models import Plantation


class Resultat(models.Model):
    plantation = models.OneToOneField(Plantation, on_delete=models.CASCADE, related_name="resultat")
    rendement_estime = models.DecimalField(max_digits=8, decimal_places=2)
    production_totale = models.DecimalField(max_digits=10, decimal_places=2)
    date_recolte_estimee = models.DateField()
    date_calcul = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Résultat de {self.plantation.nom_parcelle}"


class Risque(models.Model):
    class Niveau(models.TextChoices):
        FAIBLE = "Faible", "Faible"
        MODERE = "Modéré", "Modéré"
        ELEVE = "Élevé", "Élevé"

    resultat = models.ForeignKey(Resultat, on_delete=models.CASCADE, related_name="risques")
    niveau = models.CharField(max_length=10, choices=Niveau.choices)
    description = models.TextField()

    def __str__(self):
        return f"Risque {self.niveau} - {self.resultat.plantation.nom_parcelle}"


class Recommandation(models.Model):
    resultat = models.ForeignKey(Resultat, on_delete=models.CASCADE, related_name="recommandations")
    texte = models.TextField()

    def __str__(self):
        return f"Recommandation pour {self.resultat.plantation.nom_parcelle}"

# Create your models here.
