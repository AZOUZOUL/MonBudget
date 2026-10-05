from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.utils import timezone

from tracker.models import Categorie, Transaction
from tracker.forms import TransactionForm



def inscription(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Connecter l'utilisateur automatiquement après l'inscription
            login(request, user)
            return redirect('/') # Redirige vers la page d'accueil/tableau de bord
    else:
            form = UserCreationForm()
    return render(request, 
                      'tracker/inscription.html',
                      {"form": form})

@login_required
def demander_deconnexion(request):
    return render(request,
           'tracker/demander_deconnexion.html',)

@login_required
def deconnexion(request):
    return render(request,
                  'tracker/deconnexion.html',)
    

"""
    <<< Ceci est le code que je voulais utiliser pour
    créer une conexion personnaliser avant de savoir que ce n'est pas la peine
    >>>
    
    def log_in(request):
    if request.method == "POST":
        # 1. On remplit le formulaire avec les données saisies par l'utilisateur
        form = AuthenticationForm(request, data=request.POST)
        
        # 2. On vérifie si les identifiants respectent les règles de base
        if form.is_valid():
            # 3. On extrait le pseudo et le mot de passe nettoyés
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # 4. Le module authenticate vérifie en BDD si le couple pseudo/mot de passe est correct
            user = authenticate(username, password)
            
            if user is not None:
                # 5. Si l'utilisateur existe, la fonction login crée sa session de connexion
                login(request, user)
                return redirect('/') # Redirection vers la page d'accueil
    else:
    # Si c'est un GET, on prépare un formulaire de connexion vide
        form = AuthenticationForm()

    return render(request, 
                      'tracker/login.html',
                      {'form': form})
"""
# --- Nouvelle vue du J4 ---
@login_required
def accueil(request):
    
    #======                             =======
    #          Calcul du Mois Courant
    #======                             ========
    # Détection automatique de la date du jour réelle
    maintenant = timezone.now()
    annee_actuelle = maintenant.year
    mois_actuel = maintenant.month
    # Filtrage cumulé (Cloisonnement Utilisateur J4 + Mois en cours)
    mes_transactions_actuelles = Transaction.objects.filter(
        utilisateur=request.user,
        date__year=annee_actuelle,  # Extrait uniquement l'année en cours
        date__month=mois_actuel,  # Extrait uniquement le mois en cours
    )
    # Calculs automatiques basés uniquement sur les données du mois filtré
    entrees_actuelles = sum(transaction.montant for transaction in mes_transactions_actuelles if transaction.categorie.type == 'REV')
    depenses_actuelles = sum(transaction.montant for transaction in mes_transactions_actuelles if transaction.categorie.type == "DEP")
    solde_du_mois_actuel = entrees_actuelles - depenses_actuelles
    #======             ======
    #           Fin
    #======             ======

    return render(
        request,
        "tracker/accueil.html",
        {
            "transactions_actuelles": mes_transactions_actuelles,
            "entrees_actuelles": entrees_actuelles,
            "depenses_actuelles": depenses_actuelles,
            "solde_du_mois_actuel": solde_du_mois_actuel,
            "date_actuelle": maintenant,
        },
    )
    
@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.utilisateur = request.user
            transaction.save()
            return redirect('accueil')
    else:
        form = TransactionForm(user=request.user)
        
    return render(request,
                  'tracker/transaction_create.html',
                  {'form': form})