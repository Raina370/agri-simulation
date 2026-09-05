from django.core.management.base import BaseCommand
from agriculture.models import Region, Departement, Sol

REGIONS = [
    "Adamaoua", "Centre", "Est", "Extrême-Nord", "Littoral",
    "Nord", "Nord-Ouest", "Ouest", "Sud", "Sud-Ouest",
]

DEPARTEMENTS_OUEST = [
    "Bamboutos", "Haut-Nkam", "Hauts-Plateaux", "Koung-Khi",
    "Menoua", "Mifi", "Ndé", "Noun",
]


class Command(BaseCommand):
    help = "Seed les 10 régions du Cameroun, les départements de l'Ouest, et le sol 'Inconnu'"

    def handle(self, *args, **options):
        for nom in REGIONS:
            region, cree = Region.objects.get_or_create(nom=nom)
            self.stdout.write(f"Région {nom}: {'créée' if cree else 'existe déjà'}")

        region_ouest = Region.objects.get(nom="Ouest")
        for nom in DEPARTEMENTS_OUEST:
            departement, cree = Departement.objects.get_or_create(nom=nom, region=region_ouest)
            self.stdout.write(f"Département {nom}: {'créé' if cree else 'existe déjà'}")

        sol, cree = Sol.objects.get_or_create(
            type_sol="Inconnu",
            defaults={"description": "Type de sol non déterminé par l'utilisateur"},
        )
        self.stdout.write(f"Sol Inconnu: {'créé' if cree else 'existe déjà'}")

        self.stdout.write(self.style.SUCCESS("Seed terminé."))