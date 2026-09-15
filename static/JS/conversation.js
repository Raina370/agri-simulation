document.addEventListener('DOMContentLoaded', function () {
    const cadre = document.getElementById('chat-cadre');
    const zoneMessages = document.getElementById('chat-messages');
    const form = document.getElementById('form-message');
    const champMessage = document.getElementById('champ-message');

    if (!cadre || !zoneMessages || !form || !champMessage) {
        console.error("Chatbot : un élément attendu est introuvable dans la page.");
        return;
    }

    const conversationId = cadre.dataset.conversationId;
    const csrfInput = form.querySelector('[name=csrfmiddlewaretoken]');

    function creerLigneBulle(role, texte) {
        const ligne = document.createElement('div');
        ligne.className = 'bulle-ligne bulle-ligne-' + role;

        const avatar = document.createElement('div');
        avatar.className = 'bulle-avatar bulle-avatar-' + role;
        avatar.innerHTML = role === 'user' ? "<i class='bx bx-user'></i>" : "<i class='bx bxs-leaf'></i>";

        const bulle = document.createElement('div');
        bulle.className = 'bulle bulle-' + role;
        const p = document.createElement('p');
        p.textContent = texte;
        bulle.appendChild(p);

        ligne.appendChild(avatar);
        ligne.appendChild(bulle);
        return ligne;
    }

    function ajouterBulle(role, texte) {
        const accueil = zoneMessages.querySelector('.chat-accueil');
        if (accueil) accueil.remove();

        zoneMessages.appendChild(creerLigneBulle(role, texte));
        zoneMessages.scrollTop = zoneMessages.scrollHeight;
    }

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const texte = champMessage.value.trim();
        if (!texte) return;

        ajouterBulle('user', texte);
        champMessage.value = '';
        champMessage.disabled = true;

        const ligneChargement = document.createElement('div');
        ligneChargement.className = 'bulle-ligne bulle-ligne-assistant';
        ligneChargement.innerHTML =
            '<div class="bulle-avatar bulle-avatar-assistant"><i class="bx bxs-leaf"></i></div>' +
            '<div class="bulle bulle-assistant bulle-chargement"><span></span><span></span><span></span></div>';
        zoneMessages.appendChild(ligneChargement);
        zoneMessages.scrollTop = zoneMessages.scrollHeight;

        fetch('/assistant/' + conversationId + '/envoyer/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfInput.value,
            },
            body: 'message=' + encodeURIComponent(texte),
        })
            .then(function (reponse) {
                if (!reponse.ok) {
                    throw new Error('Statut HTTP ' + reponse.status);
                }
                return reponse.json();
            })
            .then(function (donnees) {
                ligneChargement.remove();
                ajouterBulle('assistant', donnees.reponse);
            })
            .catch(function (erreur) {
                console.error('Erreur chatbot :', erreur);
                ligneChargement.remove();
                ajouterBulle('assistant', "Une erreur est survenue, réessayez.");
            })
            .finally(function () {
                champMessage.disabled = false;
                champMessage.focus();
            });
    });

    zoneMessages.scrollTop = zoneMessages.scrollHeight;
});