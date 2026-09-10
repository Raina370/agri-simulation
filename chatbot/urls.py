from django.urls import path
from . import views

urlpatterns = [
    path("", views.liste_conversations, name="liste_conversations"),
    path("nouvelle/", views.nouvelle_conversation, name="nouvelle_conversation"),
    path("<int:pk>/", views.conversation_detail, name="conversation_detail"),
    path("<int:pk>/envoyer/", views.envoyer_message, name="envoyer_message"),
    path("<int:pk>/supprimer/", views.supprimer_conversation, name="supprimer_conversation"),
]