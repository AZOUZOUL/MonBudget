from django.db import models
from django.contrib.auth.models import User

class Categorie(models.Model):
    class Type(models.TextChoices):
            dépense = 'DEP'
            revenu = 'REV'
            
    nom = models.CharField(max_length=50)
    type = models.CharField(max_length=3, choices=Type.choices, default=Type.dépense)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom # Affichera le vrai nom dans l'admin Django
    
    @property
    def couleur(self):
        if self.type == self.Type.revenu:
            return "var(--revenu)"
        return "var(--depense)"    
