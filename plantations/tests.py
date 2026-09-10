from django.test import TestCase
from django.urls import reverse
from users.models import Utilisateur
from agriculture.models import Region, Departement, Culture, Sol
from .models import Plantation
from datetime import date, timedelta
from django.contrib.auth.hashers import make_password


class PlantationModelTest(TestCase):
    """Teste que le modèle Plantation stocke et affiche bien les données."""

    def setUp(self):
        # setUp() s'exécute automatiquement AVANT chaque test ci-dessous.
        # On y prépare des données de base réutilisables (région, culture, sol, utilisateur).
        self.region = Region.objects.create(nom="Ouest")
        self.departement = Departement.objects.create(nom="Mifi", region=self.region)
        self.culture = Culture.objects.create(
            nom="Maïs", cycle_jours=120, pluviometrie_min=800, pluviometrie_max=1200,
            temperature_min=18, temperature_max=30, rendement_moyen=5,
        )
        self.sol = Sol.objects.create(type_sol="Inconnu")
        self.utilisateur = Utilisateur.objects.create_user(
            username="testagri", password=make_password("motdepasse123"),
            date_naissance=date(1990, 1, 1), sexe="H", ville="Bafoussam",
            telephone="670000000", region="Ouest", email="test@test.com",
        )

    def test_creation_plantation(self):
        # Un test = une vérification précise. Ici : est-ce qu'une Plantation
        # se crée bien avec les bonnes valeurs ?
        plantation = Plantation.objects.create(
            utilisateur=self.utilisateur, nom_parcelle="Champ Test",
            culture=self.culture, region=self.region, departement=self.departement,
            sol=self.sol, superficie=2.5, date_plantation=date.today() + timedelta(days=5),
        )
        # assertEqual vérifie que deux valeurs sont identiques.
        # Si ce n'est pas le cas, le test échoue et affiche clairement pourquoi.
        self.assertEqual(plantation.nom_parcelle, "Champ Test")
        self.assertEqual(str(plantation), "Maïs - testagri (2.5 ha)")


class PermissionsPlantationTest(TestCase):
    """Vérifie qu'un agriculteur ne peut jamais voir les données d'un autre."""

    def setUp(self):
        self.region = Region.objects.create(nom="Ouest")
        self.departement = Departement.objects.create(nom="Mifi", region=self.region)
        self.culture = Culture.objects.create(
            nom="Maïs", cycle_jours=120, pluviometrie_min=800, pluviometrie_max=1200,
            temperature_min=18, temperature_max=30, rendement_moyen=5,
        )
        self.sol = Sol.objects.create(type_sol="Inconnu")

        self.utilisateur_a = Utilisateur.objects.create_user(
            username="agriculteur_a", password=make_password("motdepasse123"),
            date_naissance=date(1990, 1, 1), sexe="H", ville="Bafoussam",
            telephone="670000000", region="Ouest", email="a@test.com",
        )
        self.utilisateur_b = Utilisateur.objects.create_user(
            username="agriculteur_b", password=make_password("motdepasse123"),
            date_naissance=date(1990, 1, 1), sexe="F", ville="Bafoussam",
            telephone="670000001", region="Ouest", email="b@test.com",
        )

        # Une plantation appartenant à l'utilisateur A
        self.plantation_a = Plantation.objects.create(
            utilisateur=self.utilisateur_a, nom_parcelle="Champ de A",
            culture=self.culture, region=self.region, departement=self.departement,
            sol=self.sol, superficie=2.5, date_plantation=date.today() + timedelta(days=5),
        )

    def test_utilisateur_non_connecte_est_redirige(self):
        # self.client simule un vrai navigateur, sans en ouvrir un pour de vrai.
        # Ici, on visite la page SANS s'être connecté.
        reponse = self.client.get(reverse("detail_plantation", args=[self.plantation_a.pk]))
        # 302 = redirection HTTP. On s'attend à être renvoyé vers la connexion.
        self.assertEqual(reponse.status_code, 302)

    def test_b_ne_peut_pas_voir_la_plantation_de_a(self):
        # On se connecte en tant que B...
        self.client.login(username="agriculteur_b", password=make_password("motdepasse123"))
        # ...puis on essaie d'accéder à la plantation de A via son URL.
        reponse = self.client.get(reverse("detail_plantation", args=[self.plantation_a.pk]))
        # 404 = "introuvable". C'est le comportement attendu grâce à
        # get_object_or_404(..., utilisateur=request.user) dans la vue.
        self.assertEqual(reponse.status_code, 404)

    def test_a_peut_voir_sa_propre_plantation(self):
        self.client.login(username="agriculteur_a", password=make_password("motdepasse123"))
        reponse = self.client.get(reverse("detail_plantation", args=[self.plantation_a.pk]))
        # 200 = "tout va bien, la page s'affiche".
        self.assertEqual(reponse.status_code, 200)


class FormulairePlantationTest(TestCase):
    """Vérifie que les validations du formulaire fonctionnent."""

    def setUp(self):
        self.region = Region.objects.create(nom="Ouest")
        self.region_autre = Region.objects.create(nom="Nord")
        self.departement = Departement.objects.create(nom="Mifi", region=self.region)
        self.culture = Culture.objects.create(
            nom="Maïs", cycle_jours=120, pluviometrie_min=800, pluviometrie_max=1200,
            temperature_min=18, temperature_max=30, rendement_moyen=5,
        )
        self.sol = Sol.objects.create(type_sol="Inconnu")

    def test_superficie_negative_refusee(self):
        from .forms import PlantationForm
        donnees = {
            "nom_parcelle": "Test", "culture": self.culture.id, "region": self.region.id,
            "departement": self.departement.id, "sol": self.sol.id,
            "superficie": -5, "date_plantation": date.today() + timedelta(days=5),
        }
        form = PlantationForm(data=donnees)
        # is_valid() doit retourner False : une superficie négative n'a pas de sens.
        self.assertFalse(form.is_valid())

    def test_region_hors_ouest_refusee(self):
        from .forms import PlantationForm
        donnees = {
            "nom_parcelle": "Test", "culture": self.culture.id, "region": self.region_autre.id,
            "departement": self.departement.id, "sol": self.sol.id,
            "superficie": 2, "date_plantation": date.today() + timedelta(days=5),
        }
        form = PlantationForm(data=donnees)
        self.assertFalse(form.is_valid())
# Create your tests here.
