/**
 * COURS JS : SÉCURISATION DES FORMULAIRES ASYNCHRONES (ANTI-DOUBLE CLIC)
 * - Pourquoi : Éviter l'envoi de requêtes simultanées vers la base de données Django.
 * - Méthode : Utiliser une variable de contrôle `estEnCoursDeChargement` et désactiver 
 *   le bouton visuellement avec la propriété `.disabled = true`.
 */
document.addEventListener('DOMContentLoaded', function() {
    
    const modale = document.getElementById('ma-modale');
    const btnOuvrir = document.getElementById('ouvrir-modale');
    const btnFermer = document.getElementById('fermer-modale');
    const btnValider = document.getElementById('valider-categorie');
    const selectCategorie = document.getElementById('select-categorie-transaction');
    const inputNomCat = document.getElementById('nouveau-nom-cat');
    const modaleTitre = document.getElementById('modale-titre');

    // Sécurité : On s'assure que les éléments indispensables existent sur la page actuelle
    if (!modale || !btnOuvrir || !btnValider || !selectCategorie) return;

    const typeCategorie = selectCategorie.getAttribute('data-type');
    
    // VARIABLE DE SÉCURITÉ (Drapeau / Flag Anti-Bégaiement)
    let estEnCoursDeChargement = false;

    // Ouverture de la modale
    btnOuvrir.addEventListener('click', function(e) {
        e.preventDefault();
        
        if (typeCategorie === 'REV') {
            modaleTitre.textContent = "Nouvelle catégorie de revenu";
            btnValider.className = "btn-action btn-revenu";
        } else {
            modaleTitre.textContent = "Nouvelle catégorie de dépense";
            btnValider.className = "btn-action btn-depense";
        }
        
        modale.style.display = 'flex';
        inputNomCat.focus();
    });

    // Fermeture de la modale
    btnFermer.addEventListener('click', function() {
        modale.style.display = 'none';
        inputNomCat.value = '';
    });

    // Envoi de la donnée à Django
    btnValider.addEventListener('click', function(e) {
        e.preventDefault(); // Annule tout comportement par défaut du navigateur

        // 1. PROTECTION : Si une création est déjà en cours, on rejette immédiatement le clic
        if (estEnCoursDeChargement) return;

        const nomValeur = inputNomCat.value.trim();
        if (!nomValeur) {
            alert("Le nom de la catégorie ne peut pas être vide.");
            return;
        }

        // 2. VERROUILLAGE : On passe le drapeau à vrai et on désactive le bouton physiquement
        estEnCoursDeChargement = true;
        btnValider.disabled = true;
        btnValider.textContent = "Création..."; // Feedback visuel pour l'utilisateur

        const urlApi = btnValider.getAttribute('data-url');
        const csrfToken = btnValider.getAttribute('data-csrf');

        const paquetDonnees = new FormData();
        paquetDonnees.append('nom', nomValeur);
        paquetDonnees.append('type', typeCategorie);
        paquetDonnees.append('csrfmiddlewaretoken', csrfToken);

        fetch(urlApi, {
            method: 'POST',
            body: paquetDonnees
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const nouvelleOption = new Option(data.nom, data.id, true, true);
                selectCategorie.add(nouvelleOption, selectCategorie.options);
                
                modale.style.display = 'none';
                inputNomCat.value = '';
            } else {
                alert("Erreur : " + (data.error || "Impossible d'enregistrer la catégorie."));
            }
        })
        .catch(error => {
            console.error("Erreur technique :", error);
            alert("Une erreur de réseau est survenue.");
        })
        .finally(() => {
            // 3. DÉVERROUILLAGE : Quoiqu'il arrive (succès ou échec), on réactive le bouton pour la suite
            estEnCoursDeChargement = false;
            btnValider.disabled = false;
            btnValider.textContent = "Créer la catégorie";
        });
    });
});
