document.addEventListener("DOMContentLoaded", function () {

    const ecranDemarrage = document.getElementById("demarrage");

    if (!ecranDemarrage) {
        return;
    }

    /*
     * Le contenu de l'accueil est déjà chargé derrière
     * l'écran de démarrage.
     *
     * On laisse simplement le splash visible
     * pendant un court instant.
     */
    setTimeout(function () {

        ecranDemarrage.classList.add("disparition");

        /*
         * Une fois la transition terminée,
         * on retire complètement le splash du DOM.
         */
        setTimeout(function () {

            ecranDemarrage.remove();

        }, 250);

    }, 4000);

});