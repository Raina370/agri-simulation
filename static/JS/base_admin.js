document.addEventListener('DOMContentLoaded', function () {
        const burgerBtn = document.getElementById('burger-btn');
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        if (!burgerBtn || !sidebar || !overlay) return;
        function toggle() {
            sidebar.classList.toggle('sidebar-ouverte');
            overlay.classList.toggle('sidebar-overlay-visible');
        }
        burgerBtn.addEventListener('click', toggle);
        overlay.addEventListener('click', toggle);
        sidebar.querySelectorAll('a').forEach(l => l.addEventListener('click', () => {
            sidebar.classList.remove('sidebar-ouverte');
            overlay.classList.remove('sidebar-overlay-visible');
        }));
    });