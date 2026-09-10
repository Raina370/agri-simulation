from meteo.donnees_climatiques import (
    estimer_pluviometrie_cycle,
    estimer_temperature_moyenne_cycle,
)


def obtenir_conditions_climatiques(
    culture,
    date_plantation,
    departement_nom
):
    """
    Récupère les conditions climatiques estimées pour
    toute la durée du cycle de culture.
    """

    temperature = estimer_temperature_moyenne_cycle(
        departement_nom,
        date_plantation,
        culture.cycle_jours
    )

    pluie = estimer_pluviometrie_cycle(
        departement_nom,
        date_plantation,
        culture.cycle_jours
    )

    return temperature, pluie


def determiner_risque_climatique(
    culture,
    temperature_estimee,
    pluie_estimee
):
    """
    Détermine un niveau de risque climatique indépendant
    des pénalités finales.

    Valeurs retournées :
        - aucun
        - faible
        - modere
        - eleve
    """

    if temperature_estimee is None and pluie_estimee is None:
        return "eleve"

    risque_temperature = 0
    risque_pluie = 0

    # Évaluation de la température
    if temperature_estimee is not None:
        temp_min = float(culture.temperature_min)
        temp_max = float(culture.temperature_max)
        temperature = float(temperature_estimee)

        if temp_min <= temperature <= temp_max:
            risque_temperature = 0
        else:
            if temperature < temp_min:
                ecart = temp_min - temperature
            else:
                ecart = temperature - temp_max

            if ecart <= 2:
                risque_temperature = 1
            elif ecart <= 4:
                risque_temperature = 2
            else:
                risque_temperature = 3

    # Évaluation de la pluviométrie
    if pluie_estimee is not None:
        pluie_min = float(culture.pluviometrie_min)
        pluie_max = float(culture.pluviometrie_max)
        pluie = float(pluie_estimee)

        if pluie_min <= pluie <= pluie_max:
            risque_pluie = 0
        else:
            if pluie < pluie_min:
                ecart = (pluie_min - pluie) / pluie_min
            else:
                ecart = (pluie - pluie_max) / pluie_max

            if ecart <= 0.10:
                risque_pluie = 1
            elif ecart <= 0.20:
                risque_pluie = 2
            else:
                risque_pluie = 3

    niveau_max = max(risque_temperature, risque_pluie)

    if niveau_max == 0:
        return "aucun"

    if niveau_max == 1:
        return "faible"

    if niveau_max == 2:
        return "modere"

    return "eleve"


def evaluer_niveau_risque(facteur_global):
    """
    Transforme le facteur global de rendement en niveau
    de risque compréhensible par l'utilisateur.
    """

    if facteur_global >= 0.80:
        return "Faible"

    if facteur_global >= 0.60:
        return "Modéré"

    return "Élevé"