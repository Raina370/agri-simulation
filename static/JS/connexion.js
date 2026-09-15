const toggle = document.getElementById('togglePassword');
  const champMotDePasse = document.getElementById('password');
  if (toggle) {
    toggle.addEventListener('click', function () {
      const type = champMotDePasse.getAttribute('type') === 'password' ? 'text' : 'password';
      champMotDePasse.setAttribute('type', type);
      this.classList.toggle('bx-hide');
      this.classList.toggle('bx-show');
    });
  }