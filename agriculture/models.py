from django.db import models

class Region(models.Model):
    nom= models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.nom
class Departement(models.Model):
    nom=models.CharField(max_length=100)
    region= models.ForeignKey(Region, on_delete=models.CASCADE, related_name='departements')

    def __str__(self):
        return f"{self.nom} ({self.region.nom})"

class Sol(models.Model):
    type_sol=models.CharField(max_length=100, unique=True)
    description=models.TextField(blank=True)
    ph_moyen= models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True )

    def __str__(self):
        return self.type_sol

class Culture(models.Model):
    nom=models.CharField(max_length=100, unique=True)
    cycle_jours=models.PositiveBigIntegerField(help_text="Durée du cycle de culture en jours")
    pluviometrie_min = models.DecimalField(max_digits=6, decimal_places=2, help_text="En mm")
    pluviometrie_max = models.DecimalField(max_digits=6, decimal_places=2, help_text="En mm")
    temperature_min = models.DecimalField(max_digits=4, decimal_places=1, help_text="En °C")
    temperature_max = models.DecimalField(max_digits=4, decimal_places=1, help_text="En °C")
    rendement_moyen = models.DecimalField(max_digits=8, decimal_places=2, help_text="En kg/hectare ou tonnes/hectare")
    sols_compatibles = models.ManyToManyField(Sol, related_name='cultures')

    def __str__(self):
        return self.nom


# Create your models here.
