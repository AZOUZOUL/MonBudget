const boutonMenu = document.getElementById("boutonMenu");
const navigation = document.querySelector(".navigation-barre");
const liensNavigation = document.querySelector(".navigation-liens");

// Fonction pour fermer le menu
function fermerMenu() {
    navigation.classList.remove("menu-ouvert");

    boutonMenu.setAttribute("aria-expanded", "false");
    boutonMenu.setAttribute("aria-label", "Ouvrir le menu");
}

if (boutonMenu && navigation && liensNavigation) {

    // Ouvrir et fermer avec le bouton hamburger
    boutonMenu.addEventListener("click", function (event) {
        event.stopPropagation();

        const ouvert = navigation.classList.toggle("menu-ouvert");

        boutonMenu.setAttribute("aria-expanded", ouvert);
        boutonMenu.setAttribute(
            "aria-label",
            ouvert ? "Fermer le menu" : "Ouvrir le menu"
        );
    });

    // Fermer après sélection d'une page
    liensNavigation.querySelectorAll("a").forEach(function (lien) {
        lien.addEventListener("click", fermerMenu);
    });

    // Fermer lorsqu'on clique en dehors du menu
    document.addEventListener("click", function (event) {

        if (
            navigation.classList.contains("menu-ouvert") &&
            !liensNavigation.contains(event.target) &&
            !boutonMenu.contains(event.target)
        ) {
            fermerMenu();
        }

    });

}