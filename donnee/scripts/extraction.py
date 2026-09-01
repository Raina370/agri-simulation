import pdfplumber
import re
import pandas as pd
from pathlib import Path

DOSSIER_PDF = Path("donnee/pdf_source")

FICHIERS = {
    "Arachide": "Fiche Arachide.pdf",
    "Café Arabica": "Fiche Café Arabica.pdf",
    "Haricot": "Fiche Haricot.pdf",
    "Maïs": "Fiche Maïs.pdf",
    "Pomme de terre": "Fiche pomme de terre.pdf",
}


def extraire_texte(chemin_pdf):
    with pdfplumber.open(chemin_pdf) as pdf:
        texte_complet = ""
        for page in pdf.pages:
            texte_page = page.extract_text()
            if texte_page:
                texte_complet += texte_page + "\n"
        return texte_complet


def extraire_plage_numerique(texte, motif):
    """Cherche un motif du type '12–34' ou '12-34' et retourne (min, max)."""
    resultat = re.search(motif, texte)
    if resultat:
        return float(resultat.group(1).replace(",", ".")), float(resultat.group(2).replace(",", "."))
    return None, None

def extraire_texte_simple(texte, motif):
    resultat = re.search(motif, texte)
    if resultat:
        return resultat.group(1).strip()
    return None

def parser_fiche(nom_culture, texte):
    donnee = {"nom": nom_culture}

    donnee["temperature_min"], donnee["temperature_max"] = extraire_plage_numerique(
        texte, r"Température idéale\s*:\s*(\d+[.,]?\d*)[–\-](\d+[.,]?\d*)"
    )

    donnee["pluviometrie_min"], donnee["pluviometrie_max"] = extraire_plage_numerique(
        texte, r"Pluviométrie optimale\s*:\s*(\d+[.,]?\d*)[–\-](\d+[.,]?\d*)"
    )

    # Durée en jours (cultures annuelles)
    duree_min, duree_max = extraire_plage_numerique(
        texte, r"Durée de culture\s*:\s*(\d+[.,]?\d*)[–\-](\d+[.,]?\d*)"
    )
    if duree_max is not None:
        donnee["cycle_jours"] = duree_max
    else:
        # Durée en années (cultures pérennes, ex: café) -> conversion en jours
        duree_min_ans, duree_max_ans = extraire_plage_numerique(
            texte, r"Durée avant première production\s*:\s*(\d+[.,]?\d*)[–\-](\d+[.,]?\d*)"
        )
        donnee["cycle_jours"] = duree_max_ans * 365 if duree_max_ans else None

    rendement_min, rendement_max = extraire_plage_numerique(
        texte, r"Rendement moyen\s*:\s*(\d+[.,]?\d*)[–\-](\d+[.,]?\d*)"
    )
    donnee["rendement_moyen"] = rendement_max

    donnee["sols_recommandes"] = extraire_texte_simple(
        texte, r"Sols recommandés\s*:\s*(.+)"
    )

    return donnee


resultats = []
for nom_culture, nom_fichier in FICHIERS.items():
    chemin = DOSSIER_PDF / nom_fichier
    texte = extraire_texte(chemin)
    donnee = parser_fiche(nom_culture, texte)
    resultats.append(donnee)
    print(f" {nom_culture} extrait : {donnee}")

df = pd.DataFrame(resultats)
chemin_sortie = Path("donnee/csv_extraits/cultures.csv")
df.to_csv(chemin_sortie, index=False, encoding="utf-8")
print(f"\n Fichier CSV généré : {chemin_sortie}")
print(df)