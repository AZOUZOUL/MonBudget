from django.db import models
from django.contrib.auth.models import User

class Categorie(models.Model):
    class Type(models.TextChoices):
            DEPENSE = 'DEP'
            REVENU = 'REV'
            
    nom = models.CharField(max_length=50)
    type = models.CharField(max_length=3, choices=Type.choices, default=Type.DEPENSE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom # Affichera le vrai nom dans l'admin Django
    
    @property
    def couleur(self):
        if self.type == self.Type.REVENU:
            return "var(--revenu)"
        return "var(--depense)"    
class Transaction(models.Model):
    
    # Les champs
    libelle = models.CharField(max_length=120)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
    # Les liaisions inter-model
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    
    #Fonction de trie
    cree_le = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Tri automatique : d'abord par la date du budget, 
        # puis par l'ordre exact de création à égalité de date.
        # Le symbole "-" permet de trier du plus récent au plus ancien.
        ordering = ['-date', '-cree_le'] # noqa: RUF012
    
    def __str__(self):
        return self.libelle