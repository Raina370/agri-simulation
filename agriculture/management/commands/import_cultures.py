import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from agriculture.models import Culture, Sol


class Command(BaseCommand):
    help = "Importe les cultures depuis donnee/csv_extraits/cultures.csv"

    def handle(self, *args, **options):
        chemin_csv = Path("donnee/csv_extraits/cultures.csv")

        if not chemin_csv.exists():
            self.stdout.write(self.style.ERROR(f"Fichier introuvable : {chemin_csv}"))
            return

        with open(chemin_csv, encoding="utf-8") as f:
            lecteur = csv.DictReader(f)
            nb_crees = 0
            nb_maj = 0

            for ligne in lecteur:
                culture, cree = Culture.objects.update_or_create(
                    nom=ligne["nom"],
                    defaults={
                        "temperature_min": ligne["temperature_min"],
                        "temperature_max": ligne["temperature_max"],
                        "pluviometrie_min": ligne["pluviometrie_min"],
                        "pluviometrie_max": ligne["pluviometrie_max"],
                        "cycle_jours": int(float(ligne["cycle_jours"])),
                        "rendement_moyen": ligne["rendement_moyen"],
                    },
                )

                # --- Traitement des sols recommandés ---
                sols_texte = ligne.get("sols_recommandes", "")
                if sols_texte:
                    noms_sols = self.decouper_sols(sols_texte)
                    sols_objets = []
                    for nom_sol in noms_sols:
                        sol, _ = Sol.objects.get_or_create(type_sol=nom_sol.strip())
                        sols_objets.append(sol)
                    culture.sols_compatibles.set(sols_objets)

                if cree:
                    nb_crees += 1
                    self.stdout.write(self.style.SUCCESS(f" Créé : {culture.nom}"))
                else:
                    nb_maj += 1
                    self.stdout.write(self.style.WARNING(f" Mis à jour : {culture.nom}"))

        self.stdout.write(self.style.SUCCESS(f"\nTerminé : {nb_crees} créée(s), {nb_maj} mise(s) à jour."))

    def decouper_sols(self, texte):
        """Découpe une phrase de sols en types distincts, ex:
        'sols sableux ou sablo-limoneux, légers et bien drainés' -> ['sols sableux', 'sablo-limoneux']
        """
        # On coupe avant la description qualitative (après la virgule)
        partie_sols = texte.split(",")[0]
        # On sépare sur "ou"
        morceaux = partie_sols.split(" ou ")
        return [m.strip() for m in morceaux if m.strip()]