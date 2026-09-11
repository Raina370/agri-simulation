import google.generativeai as genai
from django.conf import settings

genai.configure(api_key = settings.GEMINI_API_KEY)

INSTRUCTION_SYSTEME = """Tu es l'assistant agricole d'AgriSim, une plateforme dédiée aux agriculteurs de l'Ouest Cameroun.
Réponds uniquement aux questions liées à l'agriculture : cultures, sols, climat, techniques de plantation,
lutte contre les maladies et ravageurs, irrigation, récolte, conservation.
Utilise un langage simple et pratique, adapté à des agriculteurs, pas des experts techniques.
Si une question sort du domaine agricole, réponds poliment que tu ne peux aider que sur les sujets agricoles.
Reste concis : réponses de quelques phrases, pas de longs pavés de texte."""


def generer_reponse(historique_messages, nouvelle_question):
    """
    historique_messages : liste de dicts {"role": "user"/"assistant", "contenu": "..."}
    Retourne le texte de la réponse Gemini, ou un message d'erreur clair en cas d'échec.
    """
    try:
        modele = genai.GenerativeModel(
            model_name="gemini-3.6-flash",
            system_instruction=INSTRUCTION_SYSTEME,
        )

        historique_gemini = []
        for message in historique_messages:
            role_gemini = "model" if message["role"] == "assistant" else "user"
            historique_gemini.append({"role": role_gemini, "parts": [message["contenu"]]})

        chat = modele.start_chat(history=historique_gemini)
        reponse = chat.send_message(nouvelle_question)

        return reponse.text

    except Exception as erreur:
        print("=== ERREUR GEMINI ===")
        print(repr(erreur))
        print("======================")
        return "Désolé, je n'arrive pas à répondre pour l'instant. Réessayez dans quelques instants."