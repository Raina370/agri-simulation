from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Conversation, Message
from .services import generer_reponse


@login_required
def liste_conversations(request):
    conversations = Conversation.objects.filter(utilisateur=request.user)
    return render(request, "chatbot/liste.html", {"conversations": conversations})


@login_required
def nouvelle_conversation(request):
    conversation = Conversation.objects.create(utilisateur=request.user)
    return redirect("conversation_detail", pk=conversation.pk)


@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, utilisateur=request.user)
    historique_messages = conversation.messages.all()
    return render(request, "chatbot/conversation.html", {
        "conversation": conversation,
        "historique_messages": historique_messages,
    })


@login_required
@require_POST
def envoyer_message(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, utilisateur=request.user)
    contenu = request.POST.get("message", "").strip()

    if not contenu:
        return JsonResponse({"erreur": "Message vide"}, status=400)

    Message.objects.create(conversation=conversation, role="user", contenu=contenu)

    if conversation.messages.count() == 1:
        conversation.titre = contenu[:50]
        conversation.save()

    historique = list(conversation.messages.exclude(contenu=contenu).values("role", "contenu"))
    reponse_texte = generer_reponse(historique, contenu)

    Message.objects.create(conversation=conversation, role="assistant", contenu=reponse_texte)

    return JsonResponse({
        "reponse": reponse_texte,
        "titre": conversation.titre,
    })

@login_required
def supprimer_conversation(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, utilisateur=request.user)
    if request.method == "POST":
        conversation.delete()
    return redirect("liste_conversations")