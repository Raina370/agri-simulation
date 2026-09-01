import pdfplumber
import pandas as pd
from pathlib import Path

DOSSIER_PDF = Path("donnee/pdf_source")
DOSSIER_TABLEAUX = Path("donnee/csv_extraits/tableaux")
DOSSIER_TEXTES = Path("donnee/csv_extraits/textes")
DOSSIER_TABLEAUX.mkdir(parents=True, exist_ok=True)
DOSSIER_TEXTES.mkdir(parents=True, exist_ok=True)

MOTS_CLES = {
    "cta_arabica": "CTA_ARABICA",
    "parpac_pomme_terre": "PARPAC",
    "minader_mais": "TECHNIQUE_DE_PRODUCTION",
    "ifati_mais": "MAIS.pdf",
}


def trouver_fichier(mot_cle):
    for fichier in DOSSIER_PDF.iterdir():
        if mot_cle.lower() in fichier.name.lower():
            return fichier
    return None


def extraire_document(nom_doc, chemin_pdf):
    compteur_tableaux = 0
    texte_complet = ""

    with pdfplumber.open(chemin_pdf) as pdf:
        for numero_page, page in enumerate(pdf.pages, start=1):
            texte_page = page.extract_text()
            if texte_page:
                texte_complet += f"\n--- Page {numero_page} ---\n{texte_page}\n"

            tableaux = page.extract_tables()
            for tableau in tableaux:
                if not tableau or len(tableau) < 2:
                    continue
                compteur_tableaux += 1
                df = pd.DataFrame(tableau[1:], columns=tableau[0])
                nom_fichier = f"{nom_doc}_page{numero_page}_tableau{compteur_tableaux}.csv"
                chemin_sortie = DOSSIER_TABLEAUX / nom_fichier
                df.to_csv(chemin_sortie, index=False, encoding="utf-8")
                print(f"   Tableau -> {nom_fichier}")

    chemin_texte = DOSSIER_TEXTES / f"{nom_doc}.txt"
    chemin_texte.write_text(texte_complet, encoding="utf-8")
    print(f"   Texte complet -> {chemin_texte.name}")

    if compteur_tableaux == 0:
        print(f"   Aucun tableau détecté dans {nom_doc}")

    return compteur_tableaux


for nom_doc, mot_cle in MOTS_CLES.items():
    chemin = trouver_fichier(mot_cle)
    if chemin is None:
        print(f"\n Aucun fichier trouvé pour '{nom_doc}' (mot-clé: {mot_cle})")
        continue
    print(f"\n Extraction de : {nom_doc} ({chemin.name})")
    total = extraire_document(nom_doc, chemin)
    print(f"  → {total} tableau(x) extrait(s) au total")