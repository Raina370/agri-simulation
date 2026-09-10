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
    cycle_jours=models.PositiveIntegerField(help_text="Durée du cycle de culture en jours")
    pluviometrie_min = models.DecimalField(max_digits=6, decimal_places=2, help_text="Pluviométrie minimale (mm)")
    pluviometrie_max = models.DecimalField(max_digits=6, decimal_places=2, help_text="Pluviométrie maximale (mm)")
    temperature_min = models.DecimalField(max_digits=4, decimal_places=1, help_text="Température minimale (°C)")
    temperature_max = models.DecimalField(max_digits=4, decimal_places=1, help_text="Température maximale (°C)")
    rendement_reference = models.DecimalField(max_digits=5,decimal_places=2,help_text="Rendement potentiel maximal en tonnes/hectare.")
    sols_compatibles = models.ManyToManyField(Sol, related_name='cultures')

    jour_semis_debut = models.PositiveSmallIntegerField(default=15)
    mois_semis_debut = models.PositiveSmallIntegerField(default=3)
    jour_semis_fin = models.PositiveSmallIntegerField(default=20)
    mois_semis_fin = models.PositiveSmallIntegerField(default=4)

    plafond_temperature = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.20,
        help_text="Pénalité maximale liée à la température."
    )

    plafond_pluie = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.20,
        help_text="Pénalité maximale liée à la pluviométrie."
    )

    plafond_sol = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.10,
        help_text="Pénalité maximale liée au type de sol."
    )

    plafond_date = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.15,
        help_text="Pénalité maximale liée à la date de plantation."
    )

    plafond_risque = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.15,
        help_text="Pénalité maximale liée au risque climatique."
    )

    def __str__(self):
        return self.nom


# Create your models here.
