from django.db import models
from django.conf import settings
from agriculture.models import Culture, Region, Departement, Sol

class Plantation(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='plantations')
    nom_parcelle = models.CharField(max_length=100)
    culture = models.ForeignKey(Culture, on_delete=models.PROTECT, related_name="plantations")
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="plantations")
    departement = models.ForeignKey(Departement, on_delete=models.PROTECT, related_name="plantations")
    sol = models.ForeignKey(Sol, on_delete=models.PROTECT, related_name="plantations")
    superficie = models.DecimalField(
        max_digits=8, decimal_places=2, help_text="Superficie en hectares"
    )
    date_plantation = models.DateField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.culture.nom} - {self.utilisateur.username} ({self.superficie} ha)"


# Create your models here.
