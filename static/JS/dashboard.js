    document.addEventListener('DOMContentLoaded', function () {
        const burgerBtn = document.getElementById('burger-btn');
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');

        if (!burgerBtn || !sidebar || !overlay) return;

        function ouvrirMenu() {
            sidebar.classList.add('sidebar-ouverte');
            overlay.classList.add('sidebar-overlay-visible');
            burgerBtn.innerHTML = "<i class='bx bx-x'></i>";
        }

        function fermerMenu() {
            sidebar.classList.remove('sidebar-ouverte');
            overlay.classList.remove('sidebar-overlay-visible');
            burgerBtn.innerHTML = "<i class='bx bx-menu'></i>";
        }

        burgerBtn.addEventListener('click', function () {
            if (sidebar.classList.contains('sidebar-ouverte')) {
                fermerMenu();
            } else {
                ouvrirMenu();
            }
        });

        overlay.addEventListener('click', fermerMenu);

        sidebar.querySelectorAll('a').forEach(function (lien) {
            lien.addEventListener('click', fermerMenu);
        });
    });
