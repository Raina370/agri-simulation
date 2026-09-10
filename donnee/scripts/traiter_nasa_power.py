import pandas as pd
from pathlib import Path
import pprint

DOSSIER = Path("donnee/nasa_power")

DEPARTEMENTS = {
    "Mifi": "mifi",
    "Bamboutos": "bamboutos",
    "Haut-Nkam": "haut-nkam",
    "Hauts-Plateaux": "hauts-plateaux",
    "Koung-Khi": "koung-khi",
    "Menoua": "menoua",
    "Ndé": "nde",
    "Noun": "noun",
}


def lire_csv_nasa(chemin):
    """Lit un fichier CSV NASA POWER en ignorant l'en-tête avant -END HEADER-."""
    with open(chemin, encoding="utf-8") as f:
        lignes = f.readlines()

    for i, ligne in enumerate(lignes):
        if "-END HEADER-" in ligne:
            ligne_debut = i + 1
            break
    else:
        ligne_debut = 0

    return pd.read_csv(chemin, skiprows=ligne_debut)


resultats = {}

for departement, slug in DEPARTEMENTS.items():

    chemin_meteo = DOSSIER / f"Fiche_meteo_{slug}.csv"
    chemin_precip = DOSSIER / f"precipitations_{slug}.csv"

    print(f"\nTraitement de {departement}...")

    # Lecture des fichiers
    df_meteo = lire_csv_nasa(chemin_meteo)
    df_precip = lire_csv_nasa(chemin_precip)

    # Fusion sur YEAR + DOY
    df = pd.merge(
        df_meteo,
        df_precip,
        on=["YEAR", "DOY"],
        how="inner"
    )

    # Création de la date réelle à partir de YEAR + DOY
    df["DATE"] = pd.to_datetime(
        df["YEAR"].astype(str) + df["DOY"].astype(str),
        format="%Y%j"
    )

    # Numéro du mois
    df["MO"] = df["DATE"].dt.month

    # TEMPÉRATURE MOYENNE PAR MOIS
    temp_par_mois = (
        df.groupby("MO")["T2M"]
        .mean()
        .round(1)
        .to_dict()
    )

    # DÉTECTION DE LA COLONNE DE PRÉCIPITATION
    colonne_precip = next(
        (
            c for c in df.columns
            if "PRECT" in c.upper()
            or "PRECIP" in c.upper()
        ),
        None
    )

    if colonne_precip is None:
        raise ValueError(
            f"Aucune colonne de précipitation trouvée pour {departement}. "
            f"Colonnes disponibles : {list(df.columns)}"
        )

    # PLUVIOMÉTRIE MENSUELLE
    precip_totale_mensuelle = (
        df.groupby("MO")[colonne_precip]
        .sum()
        .round(1)
        .to_dict()
    )


    # STOCKAGE DES RÉSULTATS
    resultats[departement] = {
        "temperature": temp_par_mois,
        "pluviometrie": precip_totale_mensuelle,
    }

    print(
        f"✓ {departement} traité "
        f"(précipitation : {colonne_precip})"
    )

# AFFICHAGE FINAL
print("\n" + "=" * 70)
print("RÉSULTAT À COPIER DANS donnees_climatiques.py")
print("=" * 70 + "\n")

pprint.pprint(resultats)