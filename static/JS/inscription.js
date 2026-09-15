 document.querySelectorAll('.toggle-password').forEach(function (icone) {
    icone.addEventListener('click', function () {
      const champ = document.getElementById(this.dataset.cible);
      const type = champ.getAttribute('type') === 'password' ? 'text' : 'password';
      champ.setAttribute('type', type);
      this.classList.toggle('bx-hide');
      this.classList.toggle('bx-show');
    });
  });