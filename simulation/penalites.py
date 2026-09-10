from datetime import date


"""
Fonctions de calcul des pénalités agronomiques pour AgriSim.

Chaque pénalité est exprimée sous forme décimale :
    0.10 = 10 %
    0.20 = 20 %

Les plafonds de pénalité sont définis dans le modèle Culture.
"""


def penalite_temperature(culture, temperature_estimee):
    """
    Calcule la pénalité liée à la température moyenne estimée
    pendant le cycle de culture.
    """

    temp_min = float(culture.temperature_min)
    temp_max = float(culture.temperature_max)
    plafond = float(culture.plafond_temperature)

    temperature_estimee = float(temperature_estimee)

    # Température favorable
    if temp_min <= temperature_estimee <= temp_max:
        return 0.0, (
            f"Température moyenne estimée ({temperature_estimee}°C) "
            f"dans la plage favorable "
            f"({temp_min}-{temp_max}°C)."
        )

    # Calcul de l'écart
    if temperature_estimee < temp_min:
        ecart = temp_min - temperature_estimee
        situation = "inférieure"
    else:
        ecart = temperature_estimee - temp_max
        situation = "supérieure"

    # Détermination de la pénalité
    if ecart <= 2:
        penalite = plafond * 0.25
        niveau = "léger"
    elif ecart <= 4:
        penalite = plafond * 0.50
        niveau = "modéré"
    else:
        penalite = plafond
        niveau = "important"

    return penalite, (
        f"Température moyenne estimée ({temperature_estimee}°C) "
        f"{situation} à la plage favorable : écart {niveau} "
        f"de {round(ecart, 1)}°C."
    )


def penalite_pluie(culture, pluie_estimee):
    """
    Calcule la pénalité liée à la pluviométrie estimée
    pendant le cycle de culture.
    """

    pluie_min = float(culture.pluviometrie_min)
    pluie_max = float(culture.pluviometrie_max)
    plafond = float(culture.plafond_pluie)

    pluie_estimee = float(pluie_estimee)

    # Pluviométrie favorable
    if pluie_min <= pluie_estimee <= pluie_max:
        return 0.0, (
            f"Pluviométrie estimée ({pluie_estimee} mm) "
            f"dans la plage favorable "
            f"({pluie_min}-{pluie_max} mm)."
        )

    # Pluie insuffisante
    if pluie_estimee < pluie_min:
        ecart = (pluie_min - pluie_estimee) / pluie_min
        situation = "insuffisante"

    # Pluie excessive
    else:
        ecart = (pluie_estimee - pluie_max) / pluie_max
        situation = "excessive"

    if ecart <= 0.10:
        penalite = plafond * 0.20
        niveau = "léger"
    elif ecart <= 0.20:
        penalite = plafond * 0.40
        niveau = "modéré"
    elif ecart <= 0.30:
        penalite = plafond * 0.60
        niveau = "important"
    else:
        penalite = plafond
        niveau = "très important"

    return penalite, (
        f"Pluviométrie {situation} ({pluie_estimee} mm) : "
        f"écart {niveau} par rapport à la plage favorable."
    )


def penalite_sol(culture, sol):
    """
    Calcule la pénalité liée à la compatibilité du sol.
    """

    plafond = float(culture.plafond_sol)

    if sol is None or sol.type_sol.lower() == "inconnu":
        return plafond * 0.50, (
            "Type de sol non précisé : pénalité de prudence appliquée."
        )

    sols_compatibles = culture.sols_compatibles.all()

    if sol in sols_compatibles:
        return 0.0, (
            f"Sol « {sol.type_sol} » : compatible avec "
            f"la culture de {culture.nom}."
        )

    return plafond, (
        f"Sol « {sol.type_sol} » : non compatible avec "
        f"la culture de {culture.nom}."
    )


def penalite_date_plantation(culture, date_plantation):
    """
    Calcule la pénalité liée à la date de plantation.
    """

    plafond = float(culture.plafond_date)

    annee = date_plantation.year

    debut = date(
        annee,
        culture.mois_semis_debut,
        culture.jour_semis_debut
    )

    fin = date(
        annee,
        culture.mois_semis_fin,
        culture.jour_semis_fin
    )

    # Date favorable
    if debut <= date_plantation <= fin:
        return 0.0, (
            f"Date de plantation ({date_plantation}) "
            f"dans la période favorable."
        )

    # Date trop précoce
    if date_plantation < debut:
        ecart_jours = (debut - date_plantation).days
        situation = "précoce"

    # Date trop tardive
    else:
        ecart_jours = (date_plantation - fin).days
        situation = "tardive"

    if ecart_jours <= 15:
        penalite = plafond * 0.25
        niveau = "légèrement"
    elif ecart_jours <= 30:
        penalite = plafond * 0.50
        niveau = "modérément"
    elif ecart_jours <= 45:
        penalite = plafond * 0.75
        niveau = "fortement"
    else:
        penalite = plafond
        niveau = "très fortement"

    return penalite, (
        f"Date de plantation {situation} : "
        f"{ecart_jours} jour(s) d'écart par rapport "
        f"à la période favorable."
    )


def penalite_risque_climatique(culture, risque_climatique):
    """
    Calcule une pénalité supplémentaire liée au niveau de risque
    climatique global.

    Le risque climatique ne reçoit PAS directement la pluviométrie
    afin d'éviter de pénaliser deux fois la même anomalie.
    """

    plafond = float(culture.plafond_risque)

    if risque_climatique == "aucun":
        return 0.0, (
            "Aucun risque climatique significatif détecté."
        )

    if risque_climatique == "faible":
        return plafond * 0.25, (
            "Risque climatique faible détecté."
        )

    if risque_climatique == "modere":
        return plafond * 0.50, (
            "Risque climatique modéré détecté."
        )

    if risque_climatique == "eleve":
        return plafond, (
            "Risque climatique élevé détecté."
        )

    return 0.0, (
        "Risque climatique non identifié."
    )