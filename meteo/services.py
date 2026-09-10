import requests
from django.conf import settings

VILLES_PAR_DEPARTEMENT = {
    "Bamboutos": "Mbouda",
    "Haut-Nkam": "Bafang",
    "Hauts-Plateaux": "Baham",
    "Koung-Khi": "Bandjoun",
    "Menoua": "Dschang",
    "Mifi": "Bafoussam",
    "Ndé": "Bangangté",
    "Noun": "Foumban",
}


def obtenir_meteo_actuelle(departement_nom):
    """
    Interroge OpenWeatherMap pour la ville représentative du département.
    Retourne un dictionnaire {temperature, pluviometrie_1h, description} ou None si échec.
    """
    ville = VILLES_PAR_DEPARTEMENT.get(departement_nom, "Bafoussam")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": f"{ville},CM",
        "appid": settings.OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "fr",
    }

    try:
        reponse = requests.get(url, params=params, timeout=5)
        reponse.raise_for_status()
        donnees = reponse.json()

        return {
            "ville": ville,
            "temperature": donnees["main"]["temp"],
            "pluviometrie_1h": donnees.get("rain", {}).get("1h", 0),
            "description": donnees["weather"][0]["description"],
        }
    except (requests.RequestException, KeyError):
        return None