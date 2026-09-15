document.addEventListener('DOMContentLoaded', function () {
    let elementCible = null;
    let minuteur = null;
    const DUREE_APPUI_LONG = 600;

    const modal = document.getElementById('modal-suppression');
    const btnAnnuler = document.getElementById('btn-annuler-suppression');
    const btnConfirmer = document.getElementById('btn-confirmer-suppression');

    function ouvrirModal(wrapper) {
        elementCible = wrapper;
        modal.classList.add('modal-suppression-visible');
    }

    function fermerModal() {
        elementCible = null;
        modal.classList.remove('modal-suppression-visible');
    }

    document.querySelectorAll('.carte-conversation-wrapper').forEach(function (wrapper) {
        const lien = wrapper.querySelector('.carte-conversation');

        function demarrerAppui(e) {
            minuteur = setTimeout(function () {
                if (e.cancelable) e.preventDefault();
                ouvrirModal(wrapper);
            }, DUREE_APPUI_LONG);
        }

        function annulerAppui() {
            clearTimeout(minuteur);
        }

        lien.addEventListener('mousedown', demarrerAppui);
        lien.addEventListener('mouseup', annulerAppui);
        lien.addEventListener('mouseleave', annulerAppui);
        lien.addEventListener('touchstart', demarrerAppui, { passive: true });
        lien.addEventListener('touchend', annulerAppui);
        lien.addEventListener('touchmove', annulerAppui);
    });

    btnAnnuler.addEventListener('click', fermerModal);
    modal.addEventListener('click', function (e) {
        if (e.target === modal) fermerModal();
    });

    btnConfirmer.addEventListener('click', function () {
        if (!elementCible) return;
        const form = elementCible.querySelector('.form-suppression-conversation');
        form.submit();
    });
});