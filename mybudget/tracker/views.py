from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from tracker.models import Categorie, Transaction


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
    # Filtrage pour ne recupéré que les données de l'utilisateur connecté
    mes_categories = Categorie.objects.filter(utilisateur=request.user)
    mes_transactions = Transaction.objects.filter(utilisateur=request.user)
    
    return render(request,
                  "tracker/accueil.html",
                  {'categories': mes_categories, 'transactions': mes_transactions})