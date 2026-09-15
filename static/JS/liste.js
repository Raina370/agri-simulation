document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('modal-suppression-plantation');
    const form = document.getElementById('form-suppr-plantation');
    const btnAnnuler = document.getElementById('annuler-suppr-plantation');

    document.querySelectorAll('.lien-supprimer').forEach(function (bouton) {
        bouton.addEventListener('click', function () {
            form.action = bouton.dataset.url;
            modal.classList.add('modal-suppression-visible');
        });
    });

    btnAnnuler.addEventListener('click', function () {
        modal.classList.remove('modal-suppression-visible');
    });

    modal.addEventListener('click', function (e) {
        if (e.target === modal) modal.classList.remove('modal-suppression-visible');
    });
});