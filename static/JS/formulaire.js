const messagesToasts = [
    "Merci d'avoir choisi AgriSim pour une meilleure expérience agricole",
    "Prenez le temps de remplir chaque champ. Plus vos informations sont complètes, plus les recommandations d'AgriSim seront fiables. ",
    "Choisissez une superficie réaliste. Une estimation précise de la taille de votre parcelle améliore la simulation.",
    "Renseignez la bonne date de plantation. Elle permet de croiser votre culture avec les prévisions climatiques.",
    "Sélectionnez le bon département. Les recommandations varient selon les conditions agricoles de chaque zone.",
    "Choisissez la culture de votre parcelle. Chaque culture possède des besoins climatiques et des périodes de récolte spécifiques.",
    "Connaître son type de sol améliore les résultats. Si vous le connaissez, indiquez-le pour obtenir des conseils plus précis.",
    "Les conditions météo influencent le rendement. AgriSim utilise les données climatiques pour affiner ses prévisions.",


  ];

  let indexToast = 0;

  function afficherProchainToast() {
    const conteneur = document.getElementById('conteneur-toasts');
    conteneur.innerHTML = "";

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = messagesToasts[indexToast];
    conteneur.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('toast-disparition');
      setTimeout(() => {
        toast.remove();
        indexToast = (indexToast + 1) % messagesToasts.length;
        afficherProchainToast();
      }, 1000);
    }, 7000);
  }

  afficherProchainToast();