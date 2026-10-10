from django import forms
from tracker.models import Categorie, Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        # On liste uniquement les champs à remplir
        fields = ('libelle', 'montant', 'categorie', 'date')
        
        # C'est cette bloc qui vas securisé les données en les cachants à tous sauf au proprio
    def __init__(self, *args, **kwargs):
        # Interception de l'utilisateur connecté
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
            
        # Ajout de widgets HTML5 pour un joli rendu natif
        self.fields["date"].widget = forms.DateInput(attrs={"type": "date"})

        # Si l'utilisateur existe:
        if user:
            # Filtrer et lui donner que ce qui l'appartient
            self.fields['categorie'].queryset = Categorie.objects.filter(utilisateur=user)

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ('nom', 'type')