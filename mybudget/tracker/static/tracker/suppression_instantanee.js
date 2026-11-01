/**
 * COURS JS : SUPPRESSION DYNAMIQUE SANS CHANGEMENT DE PAGE (AJAX)
 * - Pourquoi : Offrir une vitesse d'exécution maximale.
 * - location.reload() : Recharge automatiquement la page actuelle une fois la transaction 
 *   supprimée. Ainsi, le compteur de Django se met à jour et fait apparaître le bouton 
 *   "Oui, supprimer la catégorie" dès qu'il n'y a plus de transactions !
 */
document.addEventListener('DOMContentLoaded', function() {
    
    // On sélectionne tous les boutons qui possèdent notre classe spéciale
    const boutonsSuppr = document.querySelectorAll('.btn-suppr-instant');

    boutonsSuppr.forEach(bouton => {
        bouton.addEventListener('click', function(e) {
            e.preventDefault(); // Bloque le comportement naturel du lien (ne change pas de page)

            if (!confirm("Voulez-vous vraiment supprimer cette transaction immédiatement ?")) return;

            const urlApi = bouton.getAttribute('data-url');
            
            // Préparation de la requête sécurisée POST exigée par Django
            const paquet = new FormData();
            paquet.append('csrfmiddlewaretoken', window.csrfToken);

            // Envoi de l'ordre en arrière-plan au serveur Django
            fetch(urlApi, {
                method: 'POST',
                body: paquet
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Magie : On recharge la page en cours. 
                    // Django va recalculer le nombre de transactions. Dès qu'il passe à 0,
                    // l'alerte de blocage disparaît et le formulaire de suppression finale de la catégorie s'affiche !
                    location.reload();
                } else {
                    alert("Erreur : Impossible de supprimer l'opération.");
                }
            })
            .catch(error => {
                console.error("Erreur de communication :", error);
                alert("Une erreur de réseau est survenue.");
            });
        });
    });
});
