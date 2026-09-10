from datetime import timedelta

from .models import Resultat, Risque, Recommandation

from .penalites import (
    penalite_temperature,
    penalite_pluie,
    penalite_sol,
    penalite_date_plantation,
    penalite_risque_climatique,
)

from .regles import (
    obtenir_conditions_climatiques,
    determiner_risque_climatique,
    evaluer_niveau_risque,
)


def estimer_date_recolte(plantation):
    """
    Estime la date de récolte à partir de la date de plantation
    et de la durée du cycle de la culture.
    """

    return plantation.date_plantation + timedelta(
        days=plantation.culture.cycle_jours
    )


def calculer_simulation(plantation):
    """
    Effectue la simulation complète d'une plantation.

    Étapes :
        1. Récupération de la culture
        2. Estimation des conditions climatiques
        3. Calcul des pénalités
        4. Calcul du facteur global
        5. Estimation du rendement
        6. Estimation de la production totale
        7. Détermination du niveau de risque
        8. Enregistrement du résultat
        9. Enregistrement du risque
        10. Enregistrement des recommandations
    """

    culture = plantation.culture

    # ---------------------------------------------------------
    # 1. CONDITIONS CLIMATIQUES
    # ---------------------------------------------------------

    temperature_estimee, pluie_estimee = (
        obtenir_conditions_climatiques(
            culture,
            plantation.date_plantation,
            plantation.departement.nom
        )
    )

    # ---------------------------------------------------------
    # 2. CALCUL DES PÉNALITÉS
    # ---------------------------------------------------------

    penalites = []
    explications = []

    # Température
    if temperature_estimee is not None:
        penalite_temp, message_temp = penalite_temperature(
            culture,
            temperature_estimee
        )
    else:
        penalite_temp = 0.0
        message_temp = (
            "Données de température indisponibles : "
            "aucune pénalité appliquée."
        )

    penalites.append(penalite_temp)
    explications.append(message_temp)

    # Pluviométrie
    if pluie_estimee is not None:
        penalite_pluie_val, message_pluie = penalite_pluie(
            culture,
            pluie_estimee
        )
    else:
        penalite_pluie_val = 0.0
        message_pluie = (
            "Données de pluviométrie indisponibles : "
            "aucune pénalité appliquée."
        )

    penalites.append(penalite_pluie_val)
    explications.append(message_pluie)

    # Sol
    penalite_sol_val, message_sol = penalite_sol(
        culture,
        plantation.sol
    )

    penalites.append(penalite_sol_val)
    explications.append(message_sol)

    # Date de plantation
    penalite_date, message_date = penalite_date_plantation(
        culture,
        plantation.date_plantation
    )

    penalites.append(penalite_date)
    explications.append(message_date)

    # ---------------------------------------------------------
    # 3. RISQUE CLIMATIQUE
    # ---------------------------------------------------------

    risque_climatique = determiner_risque_climatique(
        culture,
        temperature_estimee,
        pluie_estimee
    )

    penalite_risque, message_risque = penalite_risque_climatique(
        culture,
        risque_climatique
    )

    penalites.append(penalite_risque)
    explications.append(message_risque)

    # ---------------------------------------------------------
    # 4. CALCUL DE LA PÉNALITÉ TOTALE
    # ---------------------------------------------------------

    penalite_totale = sum(penalites)

    # On ne peut jamais perdre plus de 100 % du rendement
    penalite_totale = min(penalite_totale, 1.0)

    facteur_global = 1.0 - penalite_totale

    # ---------------------------------------------------------
    # 5. RENDEMENT ESTIMÉ
    # ---------------------------------------------------------

    rendement_reference = float(culture.rendement_reference)

    rendement_estime = round(
        rendement_reference * facteur_global,
        2
    )

    # ---------------------------------------------------------
    # 6. PRODUCTION TOTALE
    # ---------------------------------------------------------

    superficie = float(plantation.superficie)

    production_totale = round(
        rendement_estime * superficie,
        2
    )

    # ---------------------------------------------------------
    # 7. NIVEAU DE RISQUE FINAL
    # ---------------------------------------------------------

    niveau_risque = evaluer_niveau_risque(
        facteur_global
    )

    # ---------------------------------------------------------
    # 8. DATE DE RÉCOLTE
    # ---------------------------------------------------------

    date_recolte = estimer_date_recolte(plantation)

    # ---------------------------------------------------------
    # 9. ENREGISTREMENT DU RÉSULTAT
    # ---------------------------------------------------------

    resultat, _ = Resultat.objects.update_or_create(
        plantation=plantation,
        defaults={
            "rendement_estime": rendement_estime,
            "production_totale": production_totale,
            "date_recolte_estimee": date_recolte,
        },
    )

    # ---------------------------------------------------------
    # 10. ENREGISTREMENT DU RISQUE
    # ---------------------------------------------------------

    resultat.risques.all().delete()

    Risque.objects.create(
        resultat=resultat,
        niveau=niveau_risque,
        description=message_risque
    )
    # ---------------------------------------------------------
    # 11. ENREGISTREMENT DES RECOMMANDATIONS
    # ---------------------------------------------------------

    resultat.recommandations.all().delete()

    recommandations = []

    if temperature_estimee is not None:
        if penalite_temp > 0:
            recommandations.append(
                "Surveillez les conditions de température "
                "pendant le cycle de culture."
            )

    if pluie_estimee is not None:
        if penalite_pluie_val > 0:
            if pluie_estimee < float(culture.pluviometrie_min):
                recommandations.append(
                    "Le niveau d'eau estimé à cette période ne sera pas suffisant:"
                    "si vous pouvez, prévoyez un arrosage régulier."
                )
            else:
                recommandations.append(
                    "Le niveau d'eau estimé à cette période sera trop élevé:"
                    "Pensez à faire des petits canaux pour évacuer l'eau."
                )

    if penalite_sol_val > 0:
        recommandations.append(
            "Votre sol n'est pas le plus adapté à cette culture: "
            "Si possible, améliorez-le avec du compost ou du fumier bien décomposé."
        )

    if penalite_date > 0:
        recommandations.append(
            "Votre plantation est en dehors de la période idéale:"
            "Surveillez bien les plants pendant es premières semaines."
        )

    if risque_climatique in ("modere", "eleve"):
        recommandations.append(
            "Le temps risque d'être difficile pour cette culture. "
            "Surveille régulièrement tes plants et réagis rapidement "
            "si tu vois un problème."
        )

    if not recommandations:
        recommandations.append(
            "Les conditions estimées sont favorables. "
            "Maintenez un suivi régulier de la plantation."
        )

    for texte in recommandations:
        Recommandation.objects.create(
            resultat=resultat,
            texte=texte
        )

    # ---------------------------------------------------------
    # 12. RETOUR DE LA SIMULATION
    # ---------------------------------------------------------

    return {
        "rendement_estime": rendement_estime,
        "production_totale": production_totale,
        "niveau_risque": niveau_risque,
        "date_recolte": date_recolte,
        "date_plantation": plantation.date_plantation,
        "temperature_estimee": temperature_estimee,
        "pluie_estimee": pluie_estimee,
        "risque_climatique": risque_climatique,
        "recommandations": recommandations,
    }