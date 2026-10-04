from django.contrib import admin
from tracker.models import Categorie, Transaction


class CategorieAdmin(admin.ModelAdmin):  # nous insérons ces deux lignes..
    # liste les champs que nous voulons sur l'affichage de la liste
    list_display = (
        "nom",
        "type",
        "utilisateur",
    )
    
    # Ajouté dans list_filter pour pouvoir filtrer par date de création sur le côté !
    list_filter =("utilisateur",
                  "type",
    )
admin.site.register(Categorie, CategorieAdmin)  # nous modifions cette ligne, en ajoutant un deuxième argument


class TransactionAdmin(admin.ModelAdmin):  # nous insérons ces deux lignes..
    # liste les champs que nous voulons sur l'affichage de la liste
    list_display = (
        "libelle",
        "montant",
        "categorie",
        "utilisateur",
        "date",
    ) 
    
    # Ajouté dans list_filter pour pouvoir filtrer par date de création sur le côté !
    list_filter = ("utilisateur",
                   "categorie",
                   "date",
                   "cree_le")
    #readonly_fields = ("cree_le",)
admin.site.register(Transaction, TransactionAdmin)
