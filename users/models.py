from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    class Sexe(models.TextChoices):
        HOMME = 'H','Homme'
        FEMME = 'F','Femme'

    date_naissance= models.DateField()
    sexe= models.CharField(max_length=1, choices=Sexe.choices)
    ville= models.CharField(max_length=100)
    telephone= models.CharField(max_length=20)
    region= models.CharField(max_length=100)
    description= models.TextField(blank=True)

    REQUIRED_FIELDS = ['email', 'date_naissance', 'sexe', 'ville', 'telephone', 'region']


    def __str__(self):
        return self.username
# Create your models here.
